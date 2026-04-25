"""
app/main.py
FastAPI application factory.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.constants import API_V1_PREFIX
from app.core.error_handlers import register_exception_handlers
from app.db.database import connect_db, disconnect_db

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Startup / shutdown lifecycle."""
    await connect_db()
    yield
    await disconnect_db()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Rapid Response System — Housing Societies",
        version=settings.app_version,
        description=(
            "IoT-enabled crisis management backend for housing societies. "
            "Provides one-tap emergency triggers, role-based staff alerts, "
            "real-time dashboards, micro-training drills, and post-incident analytics."
        ),
        docs_url="/docs" if not settings.is_production else None,
        redoc_url="/redoc" if not settings.is_production else None,
        openapi_url="/openapi.json" if not settings.is_production else None,
        lifespan=lifespan,
    )

    # ── CORS ──────────────────────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Exception handlers ────────────────────────────────────────────────────
    register_exception_handlers(app)

    # ── Routes ───────────────────────────────────────────────────────────────
    app.include_router(api_router, prefix=API_V1_PREFIX)

    # ── Health check (unauthenticated) ────────────────────────────────────────
    @app.get("/health", tags=["Health"], include_in_schema=False)
    async def health() -> dict:
        return {"status": "ok", "version": settings.app_version}

    return app


app = create_app()
