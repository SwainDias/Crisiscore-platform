"""
app/api/v1/admin/overview.py
GET /api/v1/admin/overview
"""

from fastapi import APIRouter, Depends, Query

from app.core.dependencies import AdminOnly, DBDep
from app.db.repositories.admin_repository import PropertyRepository, StaffDirectoryRepository
from app.db.repositories.guest_repository import GuestRepository, RoomRepository
from app.db.repositories.incident_command_repository import IncidentCommandRepository
from app.schemas.admin.overview import AdminOverviewResponse
from app.services.admin_overview_service import AdminOverviewService

router = APIRouter(prefix="/admin", tags=["Admin — Overview"])


def _get_service(db: DBDep) -> AdminOverviewService:
    return AdminOverviewService(
        property_repo=PropertyRepository(db),
        incident_repo=IncidentCommandRepository(db),
        staff_repo=StaffDirectoryRepository(db),
        guest_repo=GuestRepository(db),
        room_repo=RoomRepository(db),
    )


@router.get(
    "/overview",
    response_model=AdminOverviewResponse,
    summary="Admin Overview Dashboard",
)
async def get_admin_overview(
    current_staff: dict = AdminOnly,
    service: AdminOverviewService = Depends(_get_service),
    property_id: str | None = Query(default=None),
) -> AdminOverviewResponse:
    return await service.get_overview(property_id=property_id)
