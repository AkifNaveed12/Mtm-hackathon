from fastapi import APIRouter, HTTPException, Body
from typing import Dict, Any, Optional
from pydantic import BaseModel
from backend.app.engine.pipeline import global_engine
from backend.app.engine.tracer import global_tracer

router = APIRouter()

class RunRequest(BaseModel):
    raw_text: Optional[str] = None
    file_path: Optional[str] = None

class MessageRequest(BaseModel):
    message: str
    sender: Optional[str] = "External"

@router.post("/run")
def run_pipeline(payload: RunRequest):
    raw_text = payload.raw_text
    if not raw_text and payload.file_path:
        try:
            with open(payload.file_path, "r", encoding="utf-8") as f:
                raw_text = f.read()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Cannot read file: {e}")
            
    if not raw_text:
        # Default to sample_pack.txt
        try:
            with open("sample_pack.txt", "r", encoding="utf-8") as f:
                raw_text = f.read()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Default sample_pack.txt not found: {e}")

    plan, checks = global_engine.run_full_pipeline(raw_text)
    return {
        "status": "success",
        "plan": plan.model_dump(),
        "checks": checks.model_dump(),
        "trace": global_tracer.get_log().model_dump()
    }

@router.post("/message")
def submit_incremental_message(payload: MessageRequest):
    if not payload.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
        
    accepted, reason, plan, checks = global_engine.process_incremental_message(
        payload.message,
        payload.sender or "External"
    )
    return {
        "accepted": accepted,
        "rejection_reason": reason,
        "plan": plan.model_dump(),
        "checks": checks.model_dump(),
        "trace": global_tracer.get_log().model_dump(),
        "rejected_messages": [r.model_dump() for r in global_engine.rejected_records]
    }

@router.get("/plan")
def get_current_plan():
    return {
        "plan": global_engine.active_plan.model_dump(),
        "checks": global_engine.checks.model_dump()
    }

@router.get("/trace")
def get_trace_log():
    return global_tracer.get_log().model_dump()

@router.get("/rejected")
def get_rejected_messages():
    return [r.model_dump() for r in global_engine.rejected_records]
