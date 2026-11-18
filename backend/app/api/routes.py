from pathlib import Path
from typing import Literal
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, AliasChoices
from backend.app.engine.pipeline import global_engine
from backend.app.engine.llm import ModelFailure
from backend.app.engine.llm import provider_configured
import os

router = APIRouter()
ROOT = Path(__file__).resolve().parents[3]

class RunRequest(BaseModel):
    raw_text: str | None = Field(default=None, max_length=200000)
    file_path: str | None = Field(default=None, max_length=200)
    mode: Literal["auto", "offline", "provider"] | None = None

class MessageRequest(BaseModel):
    message: str = Field(min_length=1, max_length=20000, validation_alias=AliasChoices("message", "message_text"))
    sender: str = Field(default="External", min_length=1, max_length=120)
    mode: Literal["auto", "offline", "provider"] | None = None

def result():
    return {"plan": global_engine.active_plan.model_dump(), "checks": global_engine.checks.model_dump(),
            "trace": global_engine.tracer.get_log().model_dump(),
            "rejected_messages": [record.model_dump() for record in global_engine.rejected_records],
            "execution": global_engine.last_execution}

@router.post("/run")
def run_pipeline(payload: RunRequest):
    raw_text = payload.raw_text
    if payload.file_path:
        # The API never reads arbitrary filesystem paths. CLI alone accepts organizer file paths.
        if payload.file_path != "sample_pack.txt":
            raise HTTPException(400, "Only the bundled sample is readable by name. Upload TXT contents through raw_text.")
        if raw_text is None:
            raw_text = (ROOT / "sample_pack.txt").read_bytes().decode("utf-8")
    if raw_text is None:
        raw_text = (ROOT / "sample_pack.txt").read_bytes().decode("utf-8")
    try:
        global_engine.run_full_pipeline(raw_text, mode=payload.mode)
    except ValueError as error:
        raise HTTPException(400, str(error)) from None
    except ModelFailure as error:
        raise HTTPException(503, str(error)) from None
    response = result()
    response["status"] = "success" if global_engine.last_execution.get("status") == "completed" else "invalid"
    return response

@router.post("/message")
def submit_incremental_message(payload: MessageRequest):
    if not payload.message.strip():
        raise HTTPException(400, "Message cannot be empty.")
    try:
        accepted, reason, _, _ = global_engine.process_incremental_message(payload.message, payload.sender, payload.mode)
    except ValueError as error:
        raise HTTPException(400, str(error)) from None
    except ModelFailure as error:
        raise HTTPException(503, str(error)) from None
    return {"accepted": accepted, "rejection_reason": reason, **result()}

@router.get("/plan")
def get_current_plan():
    return {"plan": global_engine.active_plan.model_dump(), "checks": global_engine.checks.model_dump()}

@router.get("/overview")
def get_overview():
    return {**get_current_plan(), "execution": global_engine.last_execution,
            "workflow_status": global_engine.workflow_status, "message_count": len(global_engine.messages),
            "rejected_count": len(global_engine.rejected_records),
            "recent_messages": global_engine.messages[-5:]}

@router.get("/trace")
def get_trace_log():
    return global_engine.tracer.get_log().model_dump()

@router.get("/rejected")
def get_rejected_messages():
    return [record.model_dump() for record in global_engine.rejected_records]

@router.get("/messages")
def get_messages():
    return global_engine.messages

@router.get("/facts")
def get_facts():
    return {key: value for key, value in global_engine.active_facts.items() if key not in ("raw_text", "raw_messages")}

@router.get("/constraints")
def get_constraints():
    return global_engine.active_plan.constraints

@router.get("/history")
def get_history():
    return global_engine.store.history()

@router.get("/history/{version}")
def get_history_version(version: int):
    record = global_engine.store.version(version)
    if not record:
        raise HTTPException(404, "Plan version was not found.")
    return record

@router.get("/executions")
def get_executions():
    return global_engine.store.executions()

@router.get("/predict")
def predict(message: str = ""):
    areas = global_engine.predict_areas(message)
    live = os.getenv("PLANNER_MODE", "auto") != "offline" and provider_configured()
    return {"affected_areas": areas, "model_call_areas": [areas[0]] if live else [],
            "maximum_model_calls": 1, "offline_parser": not live}

@router.get("/venue")
def get_venue():
    return global_engine.active_plan.venue.model_dump()

@router.get("/schedule")
def get_schedule():
    return global_engine.active_plan.schedule.model_dump()

@router.get("/food")
def get_food():
    return global_engine.active_plan.food.model_dump()

@router.get("/judging")
def get_judging():
    return global_engine.active_plan.judging.model_dump()

@router.get("/budget")
def get_budget():
    return global_engine.active_plan.budget.model_dump()

