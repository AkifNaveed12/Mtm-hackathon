import json
from fastapi import APIRouter
from fastapi.responses import JSONResponse, PlainTextResponse
from backend.app.engine.pipeline import global_engine

router = APIRouter()

def artifact():
    return {"competition": "Mind to Machine Hackathon 2026", **global_engine.snapshot(),
            "history": global_engine.store.history()}

def markdown_report(data: dict) -> str:
    plan = data["plan"]
    lines = ["# Event planning report", "", f"Plan status: {plan['status']} | Version: {plan['version']}", "",
             "## Source facts and planning assumptions", "", json.dumps(plan.get("event", {}), ensure_ascii=False, indent=2), "",
             "Generated team/judge identifiers are assignments, not source identities. Minimum required judges are selected from the confirmed pool unless a source states otherwise.", "",
             "## Validation", ""]
    lines.extend(f"- {name}: {'PASS' if value else 'FAIL'}" for name, value in data["checks"].items() if isinstance(value, bool))
    for area in ("venue", "schedule", "food", "judging", "budget"):
        lines.extend(["", "## " + area.title(), "", "```json", json.dumps(plan[area], ensure_ascii=False, indent=2), "```"])
    lines.extend(["", "## Rejected messages", "", "```json", json.dumps(data["rejected_messages"], ensure_ascii=False, indent=2), "```",
                  "", "## Complete model trace", "", "```json", json.dumps(data["trace"], ensure_ascii=False, indent=2), "```"])
    return "\n".join(lines)

@router.get("/export")
@router.get("/export/json")
def export_submission_artifact():
    return JSONResponse(artifact(), headers={"Content-Disposition": 'attachment; filename="event-plan.json"'})

@router.get("/export/markdown")
def export_markdown():
    return PlainTextResponse(markdown_report(artifact()), media_type="text/markdown",
                             headers={"Content-Disposition": 'attachment; filename="event-plan.md"'})

@router.get("/export/trace")
def export_trace():
    return JSONResponse(global_engine.tracer.get_log().model_dump(),
                        headers={"Content-Disposition": 'attachment; filename="model-trace.json"'})

