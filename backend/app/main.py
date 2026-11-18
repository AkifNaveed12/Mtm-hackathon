from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.routes import router as core_router
from backend.app.api.health import router as health_router
from backend.app.api.export import router as export_router

app = FastAPI(
    title="HackPlan AI API",
    description="Neuro-Symbolic Agent System for Mind to Machine Hackathon Event Planning",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(core_router, prefix="/api", tags=["Core Engine"])
app.include_router(health_router, prefix="/api", tags=["Health & Status"])
app.include_router(export_router, prefix="/api", tags=["Artifact Export"])

@app.get("/")
def root():
    return {"message": "HackPlan AI Backend Online. API endpoints available under /api"}
