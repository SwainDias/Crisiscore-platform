"""
app/api/v1/router.py
Aggregates all v1 sub-routers into a single APIRouter
that main.py mounts under /api/v1.
"""

from fastapi import APIRouter

from app.api.v1.shared.app_init import router as app_init_router
from app.api.v1.shared.alert import router as alert_router
from app.api.v1.staff.auth import router as staff_auth_router
from app.api.v1.staff.home import router as staff_home_router
from app.api.v1.staff.safety_check import router as safety_check_router
from app.api.v1.staff.incident import router as incident_router
from app.api.v1.staff.drill import router as drill_router

api_router = APIRouter()

# ── Shared (staff + guest) ────────────────────────────────────────────────────
api_router.include_router(app_init_router)
api_router.include_router(alert_router)

# ── Staff ─────────────────────────────────────────────────────────────────────
api_router.include_router(staff_auth_router)
api_router.include_router(staff_home_router)
api_router.include_router(safety_check_router)
api_router.include_router(incident_router)
api_router.include_router(drill_router)
