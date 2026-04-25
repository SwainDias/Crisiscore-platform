"""
app/api/v1/guest/alert.py
GET /api/v1/guest/alert/{alert_id}/guide
"""

from fastapi import APIRouter, Depends, Header, Query

from app.core.dependencies import DBDep
from app.db.repositories.alert_repository import AlertRepository
from app.db.repositories.guest_repository import GuestRepository, RoomRepository
from app.db.repositories.incident_command_repository import IncidentCommandRepository
from app.schemas.guest.alert import GuestAlertGuideResponse
from app.services.guest_alert_guide_service import GuestAlertGuideService

router = APIRouter(prefix="/guest/alert", tags=["Guest — Alert Guide"])


def _get_service(db: DBDep) -> GuestAlertGuideService:
    return GuestAlertGuideService(
        alert_repo=AlertRepository(db),
        incident_repo=IncidentCommandRepository(db),
        guest_repo=GuestRepository(db),
        room_repo=RoomRepository(db),
    )


@router.get(
    "/{alert_id}/guide",
    response_model=GuestAlertGuideResponse,
    summary="Guest Incident Guide",
    description="Returns room-aware shelter or evacuation guidance for an active alert.",
)
async def get_guest_alert_guide(
    alert_id: str,
    service: GuestAlertGuideService = Depends(_get_service),
    guest_id: str | None = Query(default=None),
    x_guest_id: str | None = Header(default=None),
) -> GuestAlertGuideResponse:
    return await service.get_guide(alert_id=alert_id, guest_id=guest_id or x_guest_id)
