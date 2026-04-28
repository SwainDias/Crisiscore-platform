"""
app/api/v1/admin/incident.py
"""

from fastapi import APIRouter, Depends

from app.core.dependencies import AdminOnly, DBDep
from app.db.repositories.admin_repository import (
    BroadcastRepository,
    IncidentLogRepository,
    PropertyRepository,
    ResponderAssignmentRepository,
    StaffDirectoryRepository,
)
from app.db.repositories.guest_repository import GuestRepository
from app.db.repositories.incident_command_repository import IncidentCommandRepository
from app.schemas.admin.incident import (
    AdminIncidentDetailResponse,
    AdminIncidentLogRequest,
    AdminIncidentLogResponse,
    AdminIncidentResolveRequest,
    AdminIncidentResolveResponse,
    UpdateGuestStatusRequest,
    UpdateGuestStatusResponse,
)
from app.schemas.admin.map import AssignResponderRequest, AssignResponderResponse, EscalateRequest, EscalateResponse
from app.services.admin_incident_service import AdminIncidentService

router = APIRouter(prefix="/admin/incident", tags=["Admin — Incident Detail"])


def _get_service(db: DBDep) -> AdminIncidentService:
    return AdminIncidentService(
        incident_repo=IncidentCommandRepository(db),
        staff_repo=StaffDirectoryRepository(db),
        guest_repo=GuestRepository(db),
        property_repo=PropertyRepository(db),
        assignment_repo=ResponderAssignmentRepository(db),
        log_repo=IncidentLogRepository(db),
        broadcast_repo=BroadcastRepository(db),
    )


@router.get(
    "/{incident_id}",
    response_model=AdminIncidentDetailResponse,
    summary="Get Active Incident Detail",
)
async def get_incident(
    incident_id: str,
    current_staff: dict = AdminOnly,
    service: AdminIncidentService = Depends(_get_service),
) -> AdminIncidentDetailResponse:
    return await service.get_incident(incident_id)


@router.post(
    "/{incident_id}/log",
    response_model=AdminIncidentLogResponse,
    summary="Add Incident Timeline Note",
)
async def log_update(
    incident_id: str,
    payload: AdminIncidentLogRequest,
    current_staff: dict = AdminOnly,
    service: AdminIncidentService = Depends(_get_service),
) -> AdminIncidentLogResponse:
    if payload.incident_id != incident_id:
        payload.incident_id = incident_id
    return await service.log_update(incident_id, payload)


@router.post(
    "/{incident_id}/escalate",
    response_model=EscalateResponse,
    summary="Escalate Incident Severity",
)
async def escalate_incident(
    incident_id: str,
    payload: EscalateRequest,
    current_staff: dict = AdminOnly,
    service: AdminIncidentService = Depends(_get_service),
) -> EscalateResponse:
    if payload.incident_id != incident_id:
        payload.incident_id = incident_id
    return await service.escalate(payload)


@router.post(
    "/{incident_id}/resolve",
    response_model=AdminIncidentResolveResponse,
    summary="Resolve Incident",
)
async def resolve_incident(
    incident_id: str,
    payload: AdminIncidentResolveRequest,
    current_staff: dict = AdminOnly,
    service: AdminIncidentService = Depends(_get_service),
) -> AdminIncidentResolveResponse:
    if payload.incident_id != incident_id:
        payload.incident_id = incident_id
    return await service.resolve(incident_id, payload)


@router.post(
    "/{incident_id}/assign",
    response_model=AssignResponderResponse,
    summary="Assign Responder To Incident",
)
async def assign_responder(
    incident_id: str,
    payload: AssignResponderRequest,
    current_staff: dict = AdminOnly,
    service: AdminIncidentService = Depends(_get_service),
) -> AssignResponderResponse:
    if payload.incident_id != incident_id:
        payload.incident_id = incident_id
    return await service.assign_responder(payload)


@router.patch(
    "/{incident_id}/guest/{guest_id}",
    response_model=UpdateGuestStatusResponse,
    summary="Update Guest Accountability Status",
)
async def update_guest_status(
    incident_id: str,
    guest_id: str,
    payload: UpdateGuestStatusRequest,
    current_staff: dict = AdminOnly,
    service: AdminIncidentService = Depends(_get_service),
) -> UpdateGuestStatusResponse:
    return await service.update_guest_status(incident_id, guest_id, payload)
