"""All provider I/O uses httpx.MockTransport. No real WhatsApp messages are sent."""
import hashlib
import hmac
import json

import httpx
import pytest

from backend.app.integrations.whatsapp import WhatsAppError, WhatsAppService, normalize_phone


ENV = {
    "WHATSAPP_API_URL": "https://whatsapp.example.test",
    "WHATSAPP_API_KEY": "test-key-not-a-real-credential",
    "WHATSAPP_WEBHOOK_SECRET": "test-webhook-signing-secret",
}


def service(handler=None, live=False):
    env = dict(ENV, WHATSAPP_ALLOW_LIVE_SEND="true" if live else "false")
    if handler is None:
        def handler(request):
            pytest.fail("This operation must not contact any provider")
    return WhatsAppService(db_path=":memory:", env=env, transport=httpx.MockTransport(handler))


def recipient(svc, opted_in=True):
    return svc.save_recipient("Test organizer", "+923001234567", opted_in)


def notification(svc, rid, **kwargs):
    return svc.notify([rid], "schedule", "The event schedule has changed.",
                      "test-notification-key", **kwargs)


def signed(svc, data):
    body = json.dumps(data).encode()
    signature = "sha256=" + hmac.new(ENV["WHATSAPP_WEBHOOK_SECRET"].encode(), body, hashlib.sha256).hexdigest()
    return svc.process_webhook(body, signature)


@pytest.mark.parametrize("phone", ["03001234567", "923001234567", "+00123", "+92x1234567", "+123", "../secrets"])
def test_recipient_phone_rejects_invalid_values(phone):
    with pytest.raises(WhatsAppError):
        normalize_phone(phone)


def test_preview_never_calls_provider_and_is_idempotent():
    svc = service()
    rid = recipient(svc)["id"]
    first = notification(svc, rid)
    second = notification(svc, rid)
    assert first["dry_run"] and second["dry_run"]
    assert first["notifications"][0]["status"] == "preview"
    assert len(svc.notifications()) == 1


def test_opt_out_prevents_even_notification_preparation():
    svc = service()
    rid = recipient(svc, opted_in=False)["id"]
    with pytest.raises(WhatsAppError) as caught:
        notification(svc, rid)
    assert caught.value.status == 409
    assert not svc.notifications()


def test_live_send_requires_both_server_enablement_and_explicit_confirmation():
    svc = service()
    rid = recipient(svc)["id"]
    with pytest.raises(WhatsAppError) as caught:
        notification(svc, rid, dry_run=False, confirm_live_send=True)
    assert caught.value.status == 403
    enabled = service(live=True)
    rid = recipient(enabled)["id"]
    with pytest.raises(WhatsAppError):
        notification(enabled, rid, dry_run=False, confirm_live_send=False)


def test_provider_send_construction_and_no_duplicate_dispatch():
    requests = []
    def handler(request):
        requests.append(request)
        assert request.method == "POST"
        assert str(request.url) == ENV["WHATSAPP_API_URL"] + "/api/whatsapp/send"
        assert request.headers["x-api-key"] == ENV["WHATSAPP_API_KEY"]
        body = json.loads(request.content)
        assert body.get("to") == "+923001234567" and body.get("number") == "+923001234567" and body.get("message") == "The event schedule has changed."
        return httpx.Response(200, json={"success": True, "data": {"messageId": "mock-msg-1"}})
    svc = service(handler, live=True)
    rid = recipient(svc)["id"]
    first = notification(svc, rid, dry_run=False, confirm_live_send=True)
    notification(svc, rid, dry_run=False, confirm_live_send=True)
    assert len(requests) == 1
    assert first["notifications"][0]["status"] == "submitted"
    assert first["notifications"][0]["provider_message_id"] == "mock-msg-1"
    assert "delivered" not in first["notifications"][0]["status"]


def test_different_content_with_same_idempotency_key_is_rejected():
    svc = service()
    rid = recipient(svc)["id"]
    notification(svc, rid)
    with pytest.raises(WhatsAppError) as caught:
        svc.notify([rid], "schedule", "A different message.", "test-notification-key")
    assert caught.value.status == 409


def test_provider_timeout_is_unknown_and_not_retried():
    requests = []
    def handler(request):
        requests.append(request)
        raise httpx.ReadTimeout("test timeout", request=request)
    svc = service(handler, live=True)
    rid = recipient(svc)["id"]
    first = notification(svc, rid, dry_run=False, confirm_live_send=True)
    notification(svc, rid, dry_run=False, confirm_live_send=True)
    assert len(requests) == 1
    assert first["notifications"][0]["status"] == "unknown"


def test_provider_errors_are_sanitized():
    def handler(request):
        return httpx.Response(401, text="internal secret fake-sensitive-provider-value")
    svc = service(handler, live=True)
    rid = recipient(svc)["id"]
    result = notification(svc, rid, dry_run=False, confirm_live_send=True)
    assert result["notifications"][0]["status"] == "failed"
    assert "fake-sensitive-provider-value" not in json.dumps(result)
    assert ENV["WHATSAPP_API_KEY"] not in json.dumps(result)


def test_malformed_provider_json_is_a_safe_failure():
    def handler(request):
        return httpx.Response(200, json=["unexpected", "array"])
    svc = service(handler, live=True)
    assert svc.verify()["connected"] is False
    rid = recipient(svc)["id"]
    result = notification(svc, rid, dry_run=False, confirm_live_send=True)
    assert result["notifications"][0]["status"] == "failed"


def test_provider_status_verification_sends_auth_but_never_exposes_qr_or_key():
    def handler(request):
        assert request.method == "GET"
        assert request.headers["x-api-key"] == ENV["WHATSAPP_API_KEY"]
        return httpx.Response(200, json={"data": {"connected": True, "state": "connected", "qr": "sensitive-qr"}})
    svc = service(handler)
    result = svc.verify()
    assert result["connected"] is True
    assert result["provider"] == "custom_rest"
    assert "sensitive-qr" not in json.dumps(result)
    assert ENV["WHATSAPP_API_KEY"] not in json.dumps(result)


def test_webhook_signature_spoofing_rejected():
    svc = service()
    with pytest.raises(WhatsAppError) as caught:
        svc.process_webhook(b'{"event_id":"evil-event"}', "sha256=bad")
    assert caught.value.status == 401
    assert not svc.webhook_events()


def test_signed_inbound_stop_updates_consent_and_deduplicates():
    svc = service()
    recipient(svc)
    event = {"event_id": "inbound-stop-1", "direction": "inbound", "from": "+923001234567", "message": "STOP"}
    assert signed(svc, event)["duplicate"] is False
    assert svc.recipients()[0]["opted_in"] is False
    assert signed(svc, event)["duplicate"] is True
    assert len(svc.webhook_events()) == 1


def test_delivery_status_updates_are_monotonic():
    def handler(request):
        return httpx.Response(200, json={"success": True, "data": {"messageId": "mock-msg-1"}})
    svc = service(handler, live=True)
    rid = recipient(svc)["id"]
    notification(svc, rid, dry_run=False, confirm_live_send=True)
    for idx, status in enumerate(("delivered", "read", "sent")):
        signed(svc, {"event_id": f"status-{idx}", "message_id": "mock-msg-1", "status": status})
    assert svc.notifications()[0]["status"] == "read"


def test_invalid_recipient_batch_does_not_partially_persist():
    svc = service()
    rid = recipient(svc)["id"]
    with pytest.raises(WhatsAppError):
        svc.notify([rid, 999], "event", "Hello", "atomic-batch-test")
    assert not svc.notifications()


def test_send_rate_limit_enforced_with_mock_provider():
    def handler(request):
        return httpx.Response(200, json={"success": True})
    svc = service(handler, live=True)
    rid = recipient(svc)["id"]
    for index in range(5):
        svc.notify([rid], "event", "Hello", f"rate-limit-{index}", dry_run=False, confirm_live_send=True)
    with pytest.raises(WhatsAppError) as caught:
        svc.notify([rid], "event", "Hello", "rate-limit-six", dry_run=False, confirm_live_send=True)
    assert caught.value.status == 429


def test_whatsapp_records_persist_across_instances(tmp_path):
    path = tmp_path / "wa.sqlite3"
    first = WhatsAppService(db_path=path, env=ENV)
    rid = recipient(first)["id"]
    notification(first, rid)
    second = WhatsAppService(db_path=path, env=ENV)
    assert len(second.recipients()) == 1
    assert len(second.notifications()) == 1
