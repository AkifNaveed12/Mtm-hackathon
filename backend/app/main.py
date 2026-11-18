import hmac
import ipaddress
import os
import time
from collections import defaultdict, deque
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.trustedhost import TrustedHostMiddleware
from backend.app.api.routes import router as core_router
from backend.app.api.health import router as health_router
from backend.app.api.export import router as export_router
from backend.app.api.whatsapp import router as whatsapp_router

app = FastAPI(title="HackPlan AI API", description="Locally persisted event planning and verified model traces", version="2.0.0")
ALLOWED_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000"]
app.add_middleware(CORSMiddleware, allow_origins=ALLOWED_ORIGINS, allow_credentials=False,
                   allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
                   allow_headers=["Content-Type", "X-Organizer-Key", "Idempotency-Key"])
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1", "::1", "testserver"])
requests_by_client = defaultdict(deque)

@app.middleware("http")
async def local_access(request: Request, call_next):
    path = request.url.path
    webhook = path == "/api/whatsapp/webhook"
    if request.method != "OPTIONS" and path.startswith("/api/") and path != "/api/health" and not webhook:
        expected_key = os.getenv("ORGANIZER_API_KEY", "")
        if expected_key:
            if not hmac.compare_digest(request.headers.get("x-organizer-key", ""), expected_key):
                return JSONResponse({"detail": "Organizer authentication required."}, 401)
        else:
            host = request.client.host if request.client else ""
            try:
                local = ipaddress.ip_address(host).is_loopback
            except ValueError:
                local = host == "testclient"
            if not local:
                return JSONResponse({"detail": "Local access only. Configure ORGANIZER_API_KEY for authorized remote access."}, 403)
        origin = request.headers.get("origin")
        if origin and origin not in ALLOWED_ORIGINS:
            return JSONResponse({"detail": "This request origin is not permitted."}, 403)
        if request.method not in ("GET", "HEAD"):
            if int(request.headers.get("content-length", "0")) > 250000:
                return JSONResponse({"detail": "Request exceeds the 250 KB limit."}, 413)
            key = request.client.host if request.client else "unknown"
            bucket = requests_by_client[key]
            now = time.monotonic()
            while bucket and now - bucket[0] > 60:
                bucket.popleft()
            if len(bucket) >= 60:
                return JSONResponse({"detail": "Too many requests; retry after one minute."}, 429)
            bucket.append(now)
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Cache-Control"] = "no-store"
    return response

@app.exception_handler(Exception)
async def unhandled_error(request: Request, error: Exception):
    return JSONResponse({"detail": "The operation failed. Your stored plan has been preserved."}, status_code=500)

app.include_router(core_router, prefix="/api", tags=["Planning"])
app.include_router(health_router, prefix="/api", tags=["Health"])
app.include_router(export_router, prefix="/api", tags=["Exports"])
app.include_router(whatsapp_router, prefix="/api", tags=["WhatsApp"])
@app.get("/")
def root():
    return {"message": "HackPlan AI Backend Online. API endpoints available under /api"}
