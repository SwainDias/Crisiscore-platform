"""
app/api/v1/shared/app_init.py
GET /api/v1/app/init
GET /api/v1/session/system-checks
"""

from fastapi import APIRouter, Query

from app.schemas.shared.app_init import AppInitResponse, SystemChecksResponse
from app.services.app_init_service import AppInitService

router = APIRouter(tags=["App — Init & Session"])
_service = AppInitService()


@router.get(
    "/app/init",
    response_model=AppInitResponse,
    summary="App Initialisation",
    description=(
        "Called once by the client on splash screen. Returns app version, "
        "maintenance status, feature flags, and downstream service health."
    ),
)
async def app_init() -> AppInitResponse:
    return await _service.get_init()


@router.get(
    "/session/system-checks",
    response_model=SystemChecksResponse,
    summary="Session System Checks",
    description=(
        "Called after successful login for both staff and guest. Verifies all "
        "required integrations are reachable before routing the user to their home screen."
    ),
)
async def system_checks(
    user_type: str = Query(..., pattern="^(staff|guest)$"),
) -> SystemChecksResponse:
    return await _service.get_system_checks(user_type)
