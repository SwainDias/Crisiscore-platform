"""
app/api/v1/admin/map.py
"""

from fastapi import APIRouter, Depends, Query

from app.core.dependencies import AdminOnly, DBDep
from app.db.repositories.admin_repository import (
    BroadcastRepository,
    CCTVCameraRepository,
    PropertyRepository,
    ResponderAssignmentRepository,
    StaffDirectoryRepository,
)
from app.db.repositories.guest_repository import GuestRepository, RoomRepository
from app.db.repositories.incident_command_repository import IncidentCommandRepository
from app.schemas.admin.map import (
    AdminMapDataResponse,
    AssignResponderRequest,
    AssignResponderResponse,
    BroadcastRequest,
    BroadcastResponse,
    EscalateRequest,
    EscalateResponse,
)
from app.services.admin_map_service import AdminMapService

router = APIRouter(prefix="/admin", tags=["Admin — Live Map"])


def _get_service(db: DBDep) -> AdminMapService:
    return AdminMapService(
        property_repo=PropertyRepository(db),
        incident_repo=IncidentCommandRepository(db),
        staff_repo=StaffDirectoryRepository(db),
        guest_repo=GuestRepository(db),
        room_repo=RoomRepository(db),
        camera_repo=CCTVCameraRepository(db),
        assignment_repo=ResponderAssignmentRepository(db),
        broadcast_repo=BroadcastRepository(db),
    )


@router.get(
    "/map",
    response_model=AdminMapDataResponse,
    summary="Live Map Data",
)
async def get_map_data(
    current_staff: dict = AdminOnly,
    service: AdminMapService = Depends(_get_service),
    floor: int | None = Query(default=None),
    property_id: str | None = Query(default=None),
) -> AdminMapDataResponse:
    return await service.get_map_data(floor=floor, property_id=property_id)


@router.post(
    "/incident/{incident_id}/assign",
    response_model=AssignResponderResponse,
    summary="Assign Responder",
)
async def assign_responder(
    incident_id: str,
    payload: AssignResponderRequest,
    current_staff: dict = AdminOnly,
    service: AdminMapService = Depends(_get_service),
) -> AssignResponderResponse:
    if payload.incident_id != incident_id:
        payload.incident_id = incident_id
    return await service.assign_responder(payload)


@router.post(
    "/incident/{incident_id}/escalate",
    response_model=EscalateResponse,
    summary="Escalate Incident",
)
async def escalate_incident(
    incident_id: str,
    payload: EscalateRequest,
    current_staff: dict = AdminOnly,
    service: AdminMapService = Depends(_get_service),
) -> EscalateResponse:
    if payload.incident_id != incident_id:
        payload.incident_id = incident_id
    return await service.escalate(payload)


@router.post(
    "/broadcast",
    response_model=BroadcastResponse,
    summary="Broadcast Guest Message",
)
async def broadcast(
    payload: BroadcastRequest,
    current_staff: dict = AdminOnly,
    service: AdminMapService = Depends(_get_service),
    property_id: str | None = Query(default=None),
) -> BroadcastResponse:
    return await service.broadcast(payload, property_id=property_id)
