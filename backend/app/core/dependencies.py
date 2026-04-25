"""
app/core/dependencies.py
FastAPI dependency providers: DB session, current user, role guards.
"""

from typing import Annotated

from fastapi import Depends, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.constants import AuthErrorCode, StaffRole
from app.core.exceptions import ForbiddenException, UnauthorizedException
from app.core.security import decode_token
from app.db.database import get_db
from app.db.repositories.staff_repository import StaffRepository
from motor.motor_asyncio import AsyncIOMotorDatabase

_bearer = HTTPBearer(auto_error=False)


# ─── DB ──────────────────────────────────────────────────────────────────────

async def db_dependency() -> AsyncIOMotorDatabase:  # type: ignore[return]
    async for database in get_db():
        yield database


DBDep = Annotated[AsyncIOMotorDatabase, Depends(db_dependency)]


# ─── Current Staff ────────────────────────────────────────────────────────────

async def get_current_staff(
    db: DBDep,
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> dict:
    if not credentials:
        raise UnauthorizedException(
            code=AuthErrorCode.TOKEN_INVALID, message="Bearer token required."
        )
    payload = decode_token(credentials.credentials)
    if payload.get("type") != "access":
        raise UnauthorizedException(
            code=AuthErrorCode.TOKEN_INVALID, message="Invalid token type."
        )

    employee_id: str | None = payload.get("sub")
    if not employee_id:
        raise UnauthorizedException()

    repo = StaffRepository(db)
    staff = await repo.get_by_employee_id(employee_id)
    if not staff:
        raise UnauthorizedException(message="Staff member not found.")
    return staff


CurrentStaff = Annotated[dict, Depends(get_current_staff)]


# ─── Role Guards ─────────────────────────────────────────────────────────────

def require_roles(*roles: StaffRole):
    """Factory that returns a dependency enforcing role membership."""

    async def _guard(current_staff: CurrentStaff) -> dict:
        if current_staff.get("role") not in roles:
            raise ForbiddenException()
        return current_staff

    return Depends(_guard)


AdminOnly = require_roles(StaffRole.ADMIN)
SecurityOrAdmin = require_roles(StaffRole.SECURITY, StaffRole.ADMIN)
AnyStaff = require_roles(*list(StaffRole))
