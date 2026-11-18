"""Real API routes against a fresh SQLite engine for every test."""
import pytest


def test_api_root_and_health(api_client):
    assert api_client.get("/").status_code == 200
    response = api_client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "model_provider" in data
    assert "SQLite" in data["storage"]


def test_api_run_official_sample_without_fake_model_calls(api_client):
    response = api_client.post("/api/run", json={"mode": "offline"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["checks"]["all_passed"]
    assert data["plan"]["food"]["headcount"] == 177
    assert data["trace"]["total_calls"] == 0
    assert data["trace"]["entries"] == []
    assert data["trace"]["events"]


@pytest.mark.parametrize("path", ["plan", "overview", "trace", "rejected", "messages", "facts", "constraints", "history", "executions", "venue", "schedule", "food", "judging", "budget"])
def test_dashboard_endpoints_return_data(api_client, path):
    response = api_client.get("/api/" + path)
    assert response.status_code == 200
    assert isinstance(response.json(), (dict, list))
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["cache-control"] == "no-store"


def test_api_official_printing_update_and_validity(api_client):
    response = api_client.post("/api/message", json={
        "message": "Finance here. The printing bill came in at Rs 15,000, not Rs 10,000.",
        "sender": "Finance", "mode": "offline",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["accepted"]
    assert data["plan"]["budget"]["total_projected"] == 481600
    assert data["checks"]["all_passed"]


def test_api_catering_rejection_preserves_plan_and_logs_reason(api_client):
    before = api_client.get("/api/plan").json()["plan"]
    response = api_client.post("/api/message", json={
        "message": "Caterer: I have rounded your order down to 100 boxes to keep the cost low.",
        "sender": "Caterer", "mode": "offline",
    })
    assert response.status_code == 200
    data = response.json()
    assert not data["accepted"]
    assert "100" in data["rejection_reason"]
    assert data["plan"] == before
    rejected = api_client.get("/api/rejected").json()
    assert rejected[-1]["target_area"] == "food"


def test_history_keeps_previous_versions_after_change(api_client):
    before = api_client.get("/api/plan").json()["plan"]
    api_client.post("/api/message", json={"message": "Printing is now Rs 15,000.", "sender": "Finance", "mode": "offline"})
    history = api_client.get("/api/history").json()
    assert len(history) == 2
    old = api_client.get(f"/api/history/{before['version']}").json()
    assert old["plan"] == before
    assert api_client.get("/api/history/9999").status_code == 404


@pytest.mark.parametrize("path", ["/api/export", "/api/export/json", "/api/export/trace"])
def test_json_exports_are_complete_and_downloadable(api_client, path):
    response = api_client.get(path)
    assert response.status_code == 200
    assert "attachment" in response.headers["content-disposition"]
    data = response.json()
    if path.endswith("/trace"):
        assert "entries" in data and "events" in data
    else:
        assert data["competition"] == "Mind to Machine Hackathon 2026"
        for field in ("plan", "checks", "trace", "messages", "facts", "rejected_messages", "history"):
            assert field in data


def test_human_readable_report_export(api_client):
    response = api_client.get("/api/export/markdown")
    assert response.status_code == 200
    assert "text/markdown" in response.headers["content-type"]
    for area in ("Venue", "Schedule", "Food", "Judging", "Budget"):
        assert f"## {area}" in response.text
    assert "Complete model trace" in response.text


@pytest.mark.parametrize("payload,status", [
    ({"raw_text": "", "mode": "offline"}, 400),
    ({"raw_text": "x" * 200001, "mode": "offline"}, 422),
    ({"file_path": ".env", "mode": "offline"}, 400),
    ({"file_path": "../outside.txt", "mode": "offline"}, 400),
    ({"mode": "invalid-mode"}, 422),
])
def test_pack_validation_and_path_traversal_prevention(api_client, payload, status):
    before = api_client.get("/api/plan").json()
    response = api_client.post("/api/run", json=payload)
    assert response.status_code == status
    assert api_client.get("/api/plan").json() == before


def test_invalid_updates_are_validated(api_client):
    assert api_client.post("/api/message", json={"message": "   "}).status_code == 400
    assert api_client.post("/api/message", json={"message": "x" * 20001}).status_code == 422
    assert api_client.post("/api/message", json={}).status_code == 422


def test_optional_organizer_key_is_enforced_server_side(api_client, monkeypatch):
    monkeypatch.setenv("ORGANIZER_API_KEY", "unit-test-organizer-key")
    assert api_client.get("/api/plan").status_code == 401
    assert api_client.post("/api/message", json={"message": "Printing now Rs 1"}).status_code == 401
    assert api_client.get("/api/whatsapp/recipients").status_code == 401
    assert api_client.get("/api/plan", headers={"X-Organizer-Key": "wrong"}).status_code == 401
    assert api_client.get("/api/plan", headers={"X-Organizer-Key": "unit-test-organizer-key"}).status_code == 200
    assert api_client.get("/api/health").status_code == 200


def test_untrusted_origin_cannot_modify_plan(api_client):
    before = api_client.get("/api/plan").json()
    response = api_client.post("/api/message", json={"message": "Printing now Rs 1"}, headers={"Origin": "https://attacker.example"})
    assert response.status_code == 403
    assert api_client.get("/api/plan").json() == before
    assert "access-control-allow-origin" not in response.headers


def test_cors_allows_only_local_frontend(api_client):
    allowed = api_client.options("/api/run", headers={"Origin": "http://localhost:3000", "Access-Control-Request-Method": "POST"})
    assert allowed.headers["access-control-allow-origin"] == "http://localhost:3000"
    rejected = api_client.options("/api/run", headers={"Origin": "https://attacker.example", "Access-Control-Request-Method": "POST"})
    assert "access-control-allow-origin" not in rejected.headers


def test_unknown_constraints_cannot_overwrite_last_valid_plan(api_client, varied_pack):
    before = api_client.get("/api/plan").json()
    text = varied_pack + "\n# Message 8\nFrom: Director\nMessage: Teams may enter only if a safety certificate is signed.\n"
    response = api_client.post("/api/run", json={"raw_text": text, "mode": "offline"})
    assert response.status_code == 200
    assert response.json()["status"] == "invalid"
    assert api_client.get("/api/plan").json() == before


def test_prediction_is_bounded_and_relevant(api_client):
    data = api_client.get("/api/predict", params={"message": "Finance changed the printing bill"}).json()
    assert data["affected_areas"] == ["budget"]
    assert data["maximum_model_calls"] <= 5
