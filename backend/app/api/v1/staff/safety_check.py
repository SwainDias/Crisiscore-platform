"""
app/api/v1/staff/safety_check.py
GET  /api/v1/staff/safety-check
POST /api/v1/staff/safety-check/confirm
"""

from fastapi import APIRouter, Depends

from app.core.dependencies import CurrentStaff, DBDep
from app.db.repositories.safety_check_repository import SafetyCheckRepository
from app.db.repositories.staff_repository import StaffRepository
from app.schemas.staff.safety_check import (
    SafetyCheckConfirmRequest,
    SafetyCheckConfirmResponse,
    SafetyCheckResponse,
)
from app.services.safety_check_service import SafetyCheckService

router = APIRouter(prefix="/staff", tags=["Staff — Safety Check"])


def _get_service(db: DBDep) -> SafetyCheckService:
    return SafetyCheckService(SafetyCheckRepository(db), StaffRepository(db))


@router.get(
    "/safety-check",
    response_model=SafetyCheckResponse,
    summary="Get Current Safety Check",
    description=(
        "Returns the current (or newly generated) periodic safety check for the "
        "authenticated staff member, including zone info, shift elapsed time, and "
        "device health."
    ),
)
async def get_safety_check(
    current_staff: CurrentStaff,
    service: SafetyCheckService = Depends(_get_service),
) -> SafetyCheckResponse:
    return await service.get_current_check(current_staff["employee_id"])


@router.post(
    "/safety-check/confirm",
    response_model=SafetyCheckConfirmResponse,
    summary="Confirm Safety Check",
    description=(
        "Staff member confirms they are safe. Logs the confirmation timestamp "
        "and returns the time of the next scheduled check."
    ),
)
async def confirm_safety_check(
    payload: SafetyCheckConfirmRequest,
    current_staff: CurrentStaff,
    service: SafetyCheckService = Depends(_get_service),
) -> SafetyCheckConfirmResponse:
    return await service.confirm_check(payload)
