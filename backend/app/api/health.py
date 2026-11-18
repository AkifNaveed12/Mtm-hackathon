from fastapi import APIRouter
import os

router = APIRouter()

@router.get("/health")
def get_health():
    groq_configured = bool(os.getenv("GROQ_API_KEY") and not os.getenv("GROQ_API_KEY", "").startswith("your_"))
    return {
        "status": "healthy",
        "service": "HackPlan AI Backend",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "model_provider": "Groq" if groq_configured else "Deterministic Engine",
        "version": "1.0.0"
    }
