"""
app/api/v1/staff/auth.py
POST /api/v1/staff/auth/login
"""

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.dependencies import DBDep
from app.db.repositories.staff_repository import StaffRepository
from app.schemas.staff.auth import StaffLoginRequest, StaffLoginResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/staff/auth", tags=["Staff — Auth"])


def _get_service(db: DBDep) -> AuthService:
    return AuthService(StaffRepository(db))


@router.post(
    "/login",
    response_model=StaffLoginResponse,
    summary="Staff Login",
    description=(
        "Authenticates a staff member using employee ID + PIN. "
        "Optionally validates biometric token. Checks property network. "
        "Returns JWT access + refresh tokens."
    ),
)
async def staff_login(
    payload: StaffLoginRequest,
    service: AuthService = Depends(_get_service),
) -> StaffLoginResponse:
    return await service.login(payload)
