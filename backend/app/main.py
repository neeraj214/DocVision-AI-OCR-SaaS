from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .core.config import settings
from .api.routes import router
from .auth.routes import router as auth_router
from .auth.dependencies import create_db_and_tables
import os

app = FastAPI(title="DocVision AI", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Secure headers middleware
@app.middleware("http")
async def secure_headers(request: Request, call_next):
    response = await call_next(request)
    if settings.enable_secure_headers:
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["X-XSS-Protection"] = "1; mode=block"
    return response

os.makedirs(settings.output_dir, exist_ok=True)
os.makedirs(settings.tmp_dir, exist_ok=True)
os.makedirs(settings.upload_tmp_dir, exist_ok=True)
create_db_and_tables()

app.mount("/outputs", StaticFiles(directory=settings.output_dir), name="outputs")

app.include_router(router, prefix="/api")
app.include_router(auth_router)

