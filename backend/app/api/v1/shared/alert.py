"""
app/api/v1/shared/alert.py
GET  /api/v1/alert/types
POST /api/v1/alert/raise

Available to both staff and guest. Caller identity resolved from Bearer token.
"""

from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.dependencies import DBDep
from app.core.exceptions import UnauthorizedException
from app.core.security import decode_token
from app.db.repositories.alert_repository import AlertRepository, AlertTypeRepository
from app.db.repositories.incident_repository import IncidentRepository
from app.schemas.shared.alert import (
    AlertTypesResponse,
    RaiseAlertRequest,
    RaiseAlertResponse,
)
from app.services.alert_service import AlertService

router = APIRouter(prefix="/alert", tags=["Alert — Shared"])

_bearer = HTTPBearer(auto_error=False)


def _get_service(db: DBDep) -> AlertService:
    return AlertService(
        AlertRepository(db),
        AlertTypeRepository(db),
        IncidentRepository(db),
    )


async def _resolve_caller(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> dict:
    """Validates the bearer token and returns the decoded payload.
    Accepts tokens from both staff and guest auth flows."""
    if not credentials:
        raise UnauthorizedException(message="Bearer token required.")
    return decode_token(credentials.credentials)


@router.get(
    "/types",
    response_model=AlertTypesResponse,
    summary="Get Alert Types",
    description=(
        "Returns the list of available alert categories (fire, medical, security, etc.) "
        "with display metadata. Used to populate the 'Raise an Alert' screen."
    ),
)
async def get_alert_types(
    _caller: dict = Depends(_resolve_caller),
    service: AlertService = Depends(_get_service),
) -> AlertTypesResponse:
    return await service.get_alert_types()


@router.post(
    "/raise",
    response_model=RaiseAlertResponse,
    status_code=201,
    summary="Raise an Alert",
    description=(
        "Submits a new alert from a staff member or resident. Deduplicates within a "
        "5-minute window, attaches to or creates an incident for critical severity, "
        "and fans out role-based notifications."
    ),
)
async def raise_alert(
    payload: RaiseAlertRequest,
    _caller: dict = Depends(_resolve_caller),
    service: AlertService = Depends(_get_service),
) -> RaiseAlertResponse:
    return await service.raise_alert(payload)
