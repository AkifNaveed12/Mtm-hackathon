"""Consent-aware adapter for the repository's configured WhatsApp REST bot.

No network request happens at import. Sending is off unless a local operator
enables it in the environment AND explicitly confirms an individual request.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
import re
import sqlite3
import threading
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import urlsplit

import httpx
from dotenv import load_dotenv

load_dotenv()


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


class WhatsAppError(ValueError):
    def __init__(self, message: str, status: int = 400):
        super().__init__(message)
        self.status = status


def normalize_phone(value: str) -> str:
    value = value.strip()
    if not re.fullmatch(r"\+[1-9]\d{7,14}", value):
        raise WhatsAppError("Use an international phone number, for example +923001234567.")
    return value


class WhatsAppService:
    def __init__(self, db_path: str | Path | None = None,
                 env: Mapping[str, str] | None = None,
                 transport: httpx.BaseTransport | None = None):
        self.env = dict(os.environ if env is None else env)
        self.base_url = self.env.get("WHATSAPP_API_URL", "").rstrip("/")
        self.api_key = self.env.get("WHATSAPP_API_KEY", "")
        self.allow_send = self.env.get("WHATSAPP_ALLOW_LIVE_SEND", "false").lower() == "true"
        self.webhook_secret = self.env.get("WHATSAPP_WEBHOOK_SECRET", "")
        self.transport = transport
        self.db_path = str(db_path or self.env.get("WHATSAPP_DB_PATH") or
                           Path(__file__).resolve().parents[3] / "data" / "whatsapp.sqlite3")
        if self.db_path != ":memory:":
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self.lock = threading.RLock()
        self.db = sqlite3.connect(self.db_path, check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA foreign_keys=ON")
        self.verified_at: str | None = None
        self.connection_state = "not_verified"
        self.connected = False
        self.last_error: str | None = None
        with self.db:
            self.db.executescript("""
                CREATE TABLE IF NOT EXISTS recipients (
                    id INTEGER PRIMARY KEY, name TEXT NOT NULL, phone TEXT NOT NULL UNIQUE,
                    opted_in INTEGER NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS notifications (
                    id INTEGER PRIMARY KEY, recipient_id INTEGER NOT NULL REFERENCES recipients(id),
                    kind TEXT NOT NULL, message TEXT NOT NULL, status TEXT NOT NULL,
                    dry_run INTEGER NOT NULL, idempotency_key TEXT NOT NULL UNIQUE,
                    payload_hash TEXT NOT NULL, provider_message_id TEXT,
                    error TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS webhook_events (
                    id INTEGER PRIMARY KEY, event_id TEXT NOT NULL UNIQUE, event_type TEXT NOT NULL,
                    provider_message_id TEXT, recipient TEXT, status TEXT, direction TEXT,
                    message TEXT, created_at TEXT NOT NULL
                );
            """)

    @contextmanager
    def transaction(self):
        with self.lock, self.db:
            yield self.db

    @property
    def configured(self) -> bool:
        parsed = urlsplit(self.base_url)
        return bool(self.api_key and not self.api_key.startswith("your_") and
                    parsed.scheme == "https" and parsed.hostname and
                    not parsed.username and not parsed.password and not parsed.query and not parsed.fragment)

    def status(self) -> dict[str, Any]:
        missing = [k for k, value in (("WHATSAPP_API_URL", self.base_url),
                                     ("WHATSAPP_API_KEY", self.api_key)) if not value]
        blockers = []
        if not self.configured:
            blockers.append("Configure the existing HTTPS WhatsApp API URL and server-side API key.")
        if not self.allow_send:
            blockers.append("Live sending is disabled. Previews are available without contacting the provider.")
        if not self.webhook_secret:
            blockers.append("Inbound webhooks require WHATSAPP_WEBHOOK_SECRET and a signature-capable public relay.")
        blockers.append("The custom provider does not publish a template catalog or messaging-window API.")
        return {
            "provider": "custom_rest" if self.base_url else "unconfigured",
            "configured": self.configured,
            "connection_state": self.connection_state,
            "connected": self.connected,
            "verified_at": self.verified_at,
            "live_sending_enabled": self.allow_send,
            "missing_variables": missing,
            "last_error": self.last_error,
            "features": {"previews": True, "recipients": True, "consent": True,
                         "delivery_tracking": bool(self.webhook_secret),
                         "webhooks": bool(self.webhook_secret), "templates": False},
            "blockers": blockers,
        }

    def verify(self) -> dict[str, Any]:
        if not self.configured:
            raise WhatsAppError("WhatsApp server-side configuration is incomplete or is not an HTTPS URL.", 503)
        try:
            with httpx.Client(timeout=25, transport=self.transport, follow_redirects=False) as client:
                response = client.get(self.base_url + "/api/whatsapp/status",
                                      headers={"x-api-key": self.api_key})
            response.raise_for_status()
            envelope = response.json()
            if not isinstance(envelope, dict):
                raise ValueError("invalid status envelope")
            data = envelope.get("data", envelope)
            if not isinstance(data, dict):
                raise ValueError("invalid status shape")
            self.connected = data.get("connected") is True
            # Only return a bounded known state. Never forward QR codes, account IDs or raw provider errors.
            state = data.get("state", "connected" if self.connected else "disconnected")
            self.connection_state = state if state in {
                "connected", "disconnected", "connecting", "initializing", "ready", "authenticated"
            } else "unknown"
            self.last_error = None
        except httpx.TimeoutException:
            self.connected = False
            self.connection_state = "unavailable"
            self.last_error = "The WhatsApp provider timed out (cold start on Render). Please click 'Verify connection' again."
        except (httpx.HTTPError, ValueError, TypeError):
            self.connected = False
            self.connection_state = "unavailable"
            self.last_error = "The WhatsApp provider could not be verified. Check the service connection and configuration."
        self.verified_at = now()
        return self.status()

    @staticmethod
    def recipient_record(row: sqlite3.Row) -> dict[str, Any]:
        data = dict(row)
        data["opted_in"] = bool(data["opted_in"])
        return data

    def recipients(self) -> list[dict[str, Any]]:
        with self.lock:
            return [self.recipient_record(r) for r in self.db.execute("SELECT * FROM recipients ORDER BY id")]

    def save_recipient(self, name: str, phone: str, opted_in: bool) -> dict[str, Any]:
        phone = normalize_phone(phone)
        name = name.strip()
        if not 1 <= len(name) <= 120:
            raise WhatsAppError("Recipient name must contain 1 to 120 characters.")
        stamp = now()
        with self.transaction() as db:
            db.execute("""INSERT INTO recipients(name,phone,opted_in,created_at,updated_at) VALUES(?,?,?,?,?)
                ON CONFLICT(phone) DO UPDATE SET name=excluded.name,opted_in=excluded.opted_in,
                updated_at=excluded.updated_at""", (name, phone, int(opted_in), stamp, stamp))
            row = db.execute("SELECT * FROM recipients WHERE phone=?", (phone,)).fetchone()
        return self.recipient_record(row)

    def set_consent(self, recipient_id: int, opted_in: bool) -> dict[str, Any]:
        with self.transaction() as db:
            if not db.execute("SELECT id FROM recipients WHERE id=?", (recipient_id,)).fetchone():
                raise WhatsAppError("Recipient not found.", 404)
            db.execute("UPDATE recipients SET opted_in=?,updated_at=? WHERE id=?",
                       (int(opted_in), now(), recipient_id))
            row = db.execute("SELECT * FROM recipients WHERE id=?", (recipient_id,)).fetchone()
        return self.recipient_record(row)

    def notifications(self) -> list[dict[str, Any]]:
        with self.lock:
            rows = self.db.execute("""SELECT n.*,r.name AS recipient_name,r.phone AS recipient
                FROM notifications n JOIN recipients r ON r.id=n.recipient_id ORDER BY n.id DESC LIMIT 500""")
            result = []
            for row in rows:
                data = dict(row)
                data["dry_run"] = bool(data["dry_run"])
                data.pop("payload_hash", None)
                result.append(data)
            return result

    def notify(self, recipient_ids: list[int], kind: str, message: str,
               idempotency_key: str, dry_run: bool = True,
               confirm_live_send: bool = False) -> dict[str, Any]:
        if not recipient_ids or len(recipient_ids) > 20 or len(set(recipient_ids)) != len(recipient_ids):
            raise WhatsAppError("Select 1 to 20 distinct recipients.")
        if kind not in {"event", "schedule", "venue", "judging", "team", "reminder"}:
            raise WhatsAppError("Unsupported event notification type.")
        message = message.strip()
        if not 1 <= len(message) <= 4000:
            raise WhatsAppError("Notification must contain 1 to 4000 characters.")
        if not re.fullmatch(r"[A-Za-z0-9_.:-]{8,100}", idempotency_key):
            raise WhatsAppError("Use an idempotency key of 8 to 100 letters, numbers, dots, colons, underscores or hyphens.")
        if not dry_run and (not self.allow_send or not confirm_live_send):
            raise WhatsAppError("Live sends require server-side enablement and explicit organizer confirmation.", 403)
        if not dry_run and (not self.configured or len(recipient_ids) > 5):
            raise WhatsAppError("Live sending requires a configured provider and at most five recipients per request.", 403)
        digest = hashlib.sha256(json.dumps([kind, message], ensure_ascii=False).encode()).hexdigest()
        selected = []
        # Reserve unique dispatch records before network I/O. A timeout is never retried automatically.
        with self.transaction() as db:
            for recipient_id in recipient_ids:
                recipient = db.execute("SELECT * FROM recipients WHERE id=?", (recipient_id,)).fetchone()
                if not recipient:
                    raise WhatsAppError("A selected recipient does not exist.", 404)
                if not recipient["opted_in"]:
                    raise WhatsAppError("Every selected recipient must opt in before a notification can be prepared.", 409)
                key = f"{'preview' if dry_run else 'live'}:{idempotency_key}:{recipient_id}"
                existing = db.execute("SELECT * FROM notifications WHERE idempotency_key=?", (key,)).fetchone()
                if existing and existing["payload_hash"] != digest:
                    raise WhatsAppError("The idempotency key was already used with different content.", 409)
                selected.append((dict(recipient), key, existing))
            if not dry_run:
                recent = db.execute("""SELECT COUNT(*) FROM notifications WHERE dry_run=0
                    AND created_at>=?""", (datetime.fromtimestamp(time.time()-60, timezone.utc).isoformat(),)).fetchone()[0]
                new_count = sum(1 for _, _, old in selected if old is None)
                if recent + new_count > 5:
                    raise WhatsAppError("WhatsApp sending is limited to five notifications per minute.", 429)
            for recipient, key, existing in selected:
                if existing:
                    continue
                stamp = now()
                db.execute("""INSERT INTO notifications(recipient_id,kind,message,status,dry_run,
                    idempotency_key,payload_hash,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?)""",
                    (recipient["id"], kind, message, "preview" if dry_run else "dispatching",
                     int(dry_run), key, digest, stamp, stamp))
        for recipient, key, existing in selected:
            if dry_run or existing:
                continue
            status, error, provider_id = "failed", None, None
            # Check consent again just before calling a provider.
            with self.lock:
                consent = self.db.execute("SELECT opted_in FROM recipients WHERE id=?", (recipient["id"],)).fetchone()
            if not consent or not consent[0]:
                error = "Recipient opted out before dispatch."
            else:
                try:
                    with httpx.Client(timeout=25, transport=self.transport, follow_redirects=False) as client:
                        response = client.post(
                            self.base_url + "/api/whatsapp/send",
                            headers={"x-api-key": self.api_key},
                            json={
                                "number": recipient["phone"],
                                "to": recipient["phone"],
                                "message": message,
                            },
                        )
                    try:
                        envelope = response.json() if response.content else {}
                    except Exception:
                        envelope = {}
                    if not isinstance(envelope, dict):
                        raise ValueError("invalid send envelope")
                    if response.is_success and envelope.get("success") is not False:
                        data = envelope.get("data", envelope)
                        provider_id = data.get("messageId") or data.get("id") if isinstance(data, dict) else None
                        if isinstance(provider_id, dict):
                            provider_id = provider_id.get("_serialized")
                        provider_id = str(provider_id)[:250] if provider_id else None
                        status = "submitted"  # Provider acceptance is not proof of delivery.
                    else:
                        status = "failed"
                        err_obj = envelope.get("error") if isinstance(envelope, dict) else None
                        if isinstance(err_obj, dict) and err_obj.get("message"):
                            error = str(err_obj["message"])
                        elif isinstance(envelope, dict) and envelope.get("message"):
                            error = str(envelope["message"])
                        else:
                            error = f"The provider returned status code {response.status_code}."
                except httpx.TimeoutException:
                    status, error = "unknown", "Provider timed out; delivery is unknown. Do not retry without checking the provider."
                except (httpx.HTTPError, ValueError, TypeError):
                    error = "The provider request failed. Check provider status; credentials are never included in logs."
            with self.transaction() as db:
                db.execute("""UPDATE notifications SET status=?,error=?,provider_message_id=?,updated_at=?
                    WHERE idempotency_key=?""", (status, error, provider_id, now(), key))
        keys = {key for _, key, _ in selected}
        return {"dry_run": dry_run, "notifications": [n for n in self.notifications() if n["idempotency_key"] in keys]}

    def webhook_events(self) -> list[dict[str, Any]]:
        with self.lock:
            return [dict(r) for r in self.db.execute("SELECT * FROM webhook_events ORDER BY id DESC LIMIT 500")]

    def process_webhook(self, body: bytes, signature: str) -> dict[str, Any]:
        if not self.webhook_secret:
            raise WhatsAppError("Webhook signature verification is not configured.", 503)
        if len(body) > 65536:
            raise WhatsAppError("Webhook payload exceeds 64 KiB.", 413)
        expected = "sha256=" + hmac.new(self.webhook_secret.encode(), body, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected, signature):
            raise WhatsAppError("Invalid webhook signature.", 401)
        try:
            data = json.loads(body)
        except (ValueError, UnicodeDecodeError):
            raise WhatsAppError("Webhook payload must be JSON.")
        if not isinstance(data, dict):
            raise WhatsAppError("Webhook payload must be an object.")
        event_id = str(data.get("event_id") or data.get("eventId") or "")
        if not 1 <= len(event_id) <= 250:
            raise WhatsAppError("A unique event_id is required.")
        provider_id = str(data.get("message_id") or data.get("messageId") or "")[:250]
        direction = data.get("direction", "outbound")
        if direction not in {"inbound", "outbound"}:
            raise WhatsAppError("Webhook direction must be inbound or outbound.")
        status = str(data.get("status", "received" if direction == "inbound" else "unknown"))
        if status not in {"received", "sent", "delivered", "read", "failed", "unknown"}:
            raise WhatsAppError("Unsupported webhook delivery status.")
        recipient = str(data.get("from") if direction == "inbound" else data.get("to") or "")
        if recipient:
            recipient = normalize_phone(recipient)
        message = str(data.get("message") or data.get("text") or "")[:4000]
        event_type = "inbound_message" if direction == "inbound" else "delivery_status"
        with self.transaction() as db:
            if db.execute("SELECT id FROM webhook_events WHERE event_id=?", (event_id,)).fetchone():
                return {"accepted": True, "duplicate": True}
            db.execute("""INSERT INTO webhook_events(event_id,event_type,provider_message_id,recipient,
                status,direction,message,created_at) VALUES(?,?,?,?,?,?,?,?)""",
                (event_id, event_type, provider_id, recipient, status, direction, message, now()))
            if direction == "inbound" and recipient and message.strip().lower() in {"stop", "unsubscribe", "opt out", "cancel"}:
                db.execute("UPDATE recipients SET opted_in=0,updated_at=? WHERE phone=?", (now(), recipient))
            if provider_id and direction == "outbound":
                row = db.execute("SELECT id,status FROM notifications WHERE provider_message_id=?", (provider_id,)).fetchone()
                rank = {"dispatching": 0, "submitted": 1, "unknown": 1, "sent": 2, "delivered": 3, "read": 4, "failed": 5}
                if row and rank.get(status, 0) >= rank.get(row["status"], 0):
                    db.execute("UPDATE notifications SET status=?,updated_at=? WHERE id=?", (status, now(), row["id"]))
        return {"accepted": True, "duplicate": False}


_service: WhatsAppService | None = None
_service_lock = threading.Lock()


def get_service() -> WhatsAppService:
    global _service
    with _service_lock:
        if _service is None:
            _service = WhatsAppService()
    return _service
