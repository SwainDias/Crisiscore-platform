"""
app/api/v1/router.py
Aggregates all v1 sub-routers into a single APIRouter
that main.py mounts under /api/v1.
"""

from fastapi import APIRouter

from app.api.v1.admin.incident import router as admin_incident_router
from app.api.v1.admin.map import router as admin_map_router
from app.api.v1.admin.overview import router as admin_overview_router
from app.api.v1.admin.settings import router as admin_settings_router
from app.api.v1.admin.staff import router as admin_staff_router
from app.api.v1.guest.alert import router as guest_alert_router
from app.api.v1.guest.checkin import router as guest_checkin_router
from app.api.v1.guest.home import router as guest_home_router
from app.api.v1.responder.incident import router as responder_incident_router
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

# ── Guest ─────────────────────────────────────────────────────────────────────
api_router.include_router(guest_home_router)
api_router.include_router(guest_checkin_router)
api_router.include_router(guest_alert_router)

# ── Staff ─────────────────────────────────────────────────────────────────────
api_router.include_router(staff_auth_router)
api_router.include_router(staff_home_router)
api_router.include_router(safety_check_router)
api_router.include_router(incident_router)
api_router.include_router(drill_router)

# ── Responder ─────────────────────────────────────────────────────────────────
api_router.include_router(responder_incident_router)

# ── Admin ─────────────────────────────────────────────────────────────────────
api_router.include_router(admin_overview_router)
api_router.include_router(admin_map_router)
api_router.include_router(admin_incident_router)
api_router.include_router(admin_staff_router)
api_router.include_router(admin_settings_router)
