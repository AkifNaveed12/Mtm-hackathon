from fastapi import APIRouter
from fastapi.responses import JSONResponse
from backend.app.engine.pipeline import global_engine
from backend.app.engine.tracer import global_tracer

router = APIRouter()

@router.get("/export")
def export_submission_artifact():
    """Generates official plan, 6 checks, and full trace for competition submission."""
    return JSONResponse(content={
        "competition": "Mind to Machine Hackathon 2026",
        "plan": global_engine.active_plan.model_dump(),
        "checks": global_engine.checks.model_dump(),
        "trace": global_tracer.get_log().model_dump(),
        "rejected_messages": [r.model_dump() for r in global_engine.rejected_records]
    })
