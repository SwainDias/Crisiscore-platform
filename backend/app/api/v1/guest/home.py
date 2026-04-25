"""
app/api/v1/guest/home.py
GET /api/v1/guest/home
"""

from fastapi import APIRouter, Depends, Header, Query

from app.core.dependencies import DBDep
from app.db.repositories.admin_repository import PropertyRepository
from app.db.repositories.guest_repository import GuestRepository
from app.db.repositories.incident_command_repository import IncidentCommandRepository
from app.schemas.guest.home import GuestHomeResponse
from app.services.guest_home_service import GuestHomeService

router = APIRouter(prefix="/guest", tags=["Guest — Home"])


def _get_service(db: DBDep) -> GuestHomeService:
    return GuestHomeService(
        guest_repo=GuestRepository(db),
        property_repo=PropertyRepository(db),
        incident_repo=IncidentCommandRepository(db),
    )


@router.get(
    "/home",
    response_model=GuestHomeResponse,
    summary="Guest Home",
    description=(
        "Guest-facing home payload with active alerts, quick actions, and safety info hub."
    ),
)
async def get_guest_home(
    service: GuestHomeService = Depends(_get_service),
    guest_id: str | None = Query(default=None),
    x_guest_id: str | None = Header(default=None),
) -> GuestHomeResponse:
    return await service.get_home(guest_id or x_guest_id)
