"""
app/api/v1/staff/home.py
GET  /api/v1/staff/home
POST /api/v1/staff/sos
"""

from fastapi import APIRouter, Depends

from app.core.dependencies import CurrentStaff, DBDep
from app.db.repositories.incident_repository import IncidentRepository
from app.db.repositories.staff_repository import StaffRepository
from app.db.repositories.task_repository import TaskRepository
from app.schemas.staff.home import (
    SOSTriggerRequest,
    SOSTriggerResponse,
    StaffHomeResponse,
)
from app.services.staff_home_service import StaffHomeService

router = APIRouter(prefix="/staff", tags=["Staff — Home"])


def _get_service(db: DBDep) -> StaffHomeService:
    return StaffHomeService(
        StaffRepository(db),
        IncidentRepository(db),
        TaskRepository(db),
    )


@router.get(
    "/home",
    response_model=StaffHomeResponse,
    summary="Staff Home / Status Dashboard",
    description=(
        "Returns the complete dashboard payload for the authenticated staff member: "
        "active incident banner, duty status, live map summary, tasks, and recent history."
    ),
)
async def get_staff_home(
    current_staff: CurrentStaff,
    service: StaffHomeService = Depends(_get_service),
) -> StaffHomeResponse:
    return await service.get_home(current_staff["employee_id"])


@router.post(
    "/sos",
    response_model=SOSTriggerResponse,
    summary="Trigger SOS Broadcast",
    description=(
        "Broadcasts a silent or audible SOS from the authenticated staff member's "
        "current location to all security personnel and management."
    ),
)
async def trigger_sos(
    payload: SOSTriggerRequest,
    current_staff: CurrentStaff,
    service: StaffHomeService = Depends(_get_service),
) -> SOSTriggerResponse:
    return await service.trigger_sos(payload)
