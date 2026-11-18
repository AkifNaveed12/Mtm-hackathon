import os
from fastapi import APIRouter
from backend.app.engine.llm import provider_configured
router = APIRouter()
@router.get("/health")
def get_health():
    return {"status": "healthy", "service": "HackPlan AI Backend", "version": "2.0.0",
            "environment": os.getenv("ENVIRONMENT", "development"),
            "model_provider": "Groq" if provider_configured() else "Offline parser",
            "model": os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b") if provider_configured() else None,
            "provider_configured": provider_configured(), "organizer_key_required": bool(os.getenv("ORGANIZER_API_KEY")),
            "default_mode": os.getenv("PLANNER_MODE", "auto"), "workflow": "LangGraph", "storage": "SQLite"}

