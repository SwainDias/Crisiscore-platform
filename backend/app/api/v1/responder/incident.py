"""
app/api/v1/responder/incident.py
"""

from fastapi import APIRouter, Depends

from app.core.dependencies import AnyStaff, DBDep
from app.db.repositories.admin_repository import IncidentLogRepository
from app.db.repositories.incident_command_repository import IncidentCommandRepository
from app.schemas.responder.incident import (
    BackupRequestResponse,
    LogUpdateRequest,
    LogUpdateResponse,
    ResolveRequest,
    ResolveResponse,
    ResponderIncidentResponse,
)
from app.services.responder_incident_service import ResponderIncidentService

router = APIRouter(prefix="/responder/incident", tags=["Responder — Incident"])


def _get_service(db: DBDep) -> ResponderIncidentService:
    return ResponderIncidentService(
        incident_repo=IncidentCommandRepository(db),
        log_repo=IncidentLogRepository(db),
    )


@router.get(
    "/{incident_id}",
    response_model=ResponderIncidentResponse,
    summary="Responder Incident Dashboard",
)
async def get_incident(
    incident_id: str,
    current_staff: dict = AnyStaff,
    service: ResponderIncidentService = Depends(_get_service),
) -> ResponderIncidentResponse:
    return await service.get_incident(incident_id)


@router.post(
    "/{incident_id}/backup",
    response_model=BackupRequestResponse,
    summary="Request Backup",
)
async def request_backup(
    incident_id: str,
    current_staff: dict = AnyStaff,
    service: ResponderIncidentService = Depends(_get_service),
) -> BackupRequestResponse:
    return await service.request_backup(incident_id, current_staff["employee_id"])


@router.post(
    "/{incident_id}/log",
    response_model=LogUpdateResponse,
    summary="Log Responder Update",
)
async def log_update(
    incident_id: str,
    payload: LogUpdateRequest,
    current_staff: dict = AnyStaff,
    service: ResponderIncidentService = Depends(_get_service),
) -> LogUpdateResponse:
    return await service.log_update(incident_id, payload)


@router.post(
    "/{incident_id}/resolve",
    response_model=ResolveResponse,
    summary="Resolve Incident",
)
async def resolve_incident(
    incident_id: str,
    payload: ResolveRequest,
    current_staff: dict = AnyStaff,
    service: ResponderIncidentService = Depends(_get_service),
) -> ResolveResponse:
    return await service.resolve(incident_id, payload)
