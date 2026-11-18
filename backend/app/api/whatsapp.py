"""Local organizer endpoints. Authentication is enforced by application middleware."""
from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, Header, HTTPException, Request
from pydantic import BaseModel, ConfigDict, Field

from backend.app.integrations.whatsapp import WhatsAppError, get_service

router = APIRouter(prefix="/whatsapp", tags=["WhatsApp"])


class StrictRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class RecipientRequest(StrictRequest):
    name: str = Field(min_length=1, max_length=120)
    phone: str = Field(pattern=r"^\+[1-9]\d{7,14}$")
    opted_in: bool = False


class ConsentRequest(StrictRequest):
    opted_in: bool


class NotificationRequest(StrictRequest):
    recipient_ids: list[int] = Field(min_length=1, max_length=20)
    kind: Literal["event", "schedule", "venue", "judging", "team", "reminder"] = "event"
    message: str = Field(min_length=1, max_length=4000)
    idempotency_key: str = Field(pattern=r"^[A-Za-z0-9_.:-]{8,100}$")
    dry_run: bool = True
    confirm_live_send: bool = False


def execute(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except WhatsAppError as exc:
        raise HTTPException(status_code=exc.status, detail=str(exc)) from None


@router.get("/status")
def status():
    return get_service().status()


@router.post("/status/verify")
def verify():
    return execute(get_service().verify)


@router.get("/recipients")
def recipients():
    return get_service().recipients()


@router.post("/recipients")
def save_recipient(payload: RecipientRequest):
    return execute(get_service().save_recipient, **payload.model_dump())


@router.patch("/recipients/{recipient_id}")
def consent(recipient_id: int, payload: ConsentRequest):
    return execute(get_service().set_consent, recipient_id, payload.opted_in)


@router.get("/messages")
def messages():
    return get_service().notifications()


@router.get("/templates")
def templates():
    return {"templates": [], "supported": False,
            "reason": "The configured custom WhatsApp bot does not advertise approved templates or messaging-window rules."}


@router.get("/webhooks")
def events():
    return get_service().webhook_events()


@router.post("/notifications")
def notifications(payload: NotificationRequest):
    return execute(get_service().notify, **payload.model_dump())


@router.post("/webhook")
async def webhook(request: Request,
                  x_whatsapp_signature: str = Header(default=""),
                  x_hub_signature_256: str = Header(default="")):
    body = bytearray()
    async for chunk in request.stream():
        body.extend(chunk)
        if len(body) > 65536:
            raise HTTPException(status_code=413, detail="Webhook payload exceeds 64 KiB.")
    return execute(get_service().process_webhook, bytes(body), x_whatsapp_signature or x_hub_signature_256)
