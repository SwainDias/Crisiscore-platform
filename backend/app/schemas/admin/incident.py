"""
app/schemas/admin/incident.py
"""

from typing import Literal

from pydantic import BaseModel

from app.core.constants import (
    CrisisPriority,
    ExternalService,
    ExternalServiceStatus,
    GuestAccountabilityStatus,
    IncidentStatus,
    IncidentType,
)
from app.schemas.admin.map import BroadcastRequest, BroadcastResponse


class AdminIncidentLocation(BaseModel):
    property: str
    building: str
    zone: str
    floor: int


class ResponderPin(BaseModel):
    label: str
    lat: float
    lng: float


class SweepZone(BaseModel):
    zone_id: str
    label: str
    lat: float
    lng: float
    width: float
    height: float


class TacticalMap(BaseModel):
    floor: int
    responder_pins: list[ResponderPin]
    incident_pin: ResponderPin
    sweep_zones: list[SweepZone]


class ResponderAssignment(BaseModel):
    employee_id: str
    name: str
    role: str
    team: str | None = None
    status: Literal["on_scene", "en_route", "standby"]
    eta_seconds: int | None = None


class GuestAccountabilityItem(BaseModel):
    guest_id: str
    room: str
    name: str
    status: GuestAccountabilityStatus


class ExternalServiceItem(BaseModel):
    service: ExternalService
    status: ExternalServiceStatus
    eta_seconds: int | None = None


class BroadcastTemplate(BaseModel):
    template_id: str
    label: str
    body: str


class TimelineItem(BaseModel):
    event_id: str
    timestamp: str
    description: str
    icon: str


class AdminIncidentDetailResponse(BaseModel):
    incident_id: str
    event_code: str
    severity: CrisisPriority
    status: IncidentStatus
    type: IncidentType
    title: str
    location: AdminIncidentLocation
    elapsed_seconds: int
    responders_on_scene: int
    guests_unaccounted: int
    services_notified: list[Literal["fire", "police", "medical"]]
    sop_progress_percent: float
    tactical_map: TacticalMap
    responder_assignments: list[ResponderAssignment]
    guest_accountability: list[GuestAccountabilityItem]
    external_services: list[ExternalServiceItem]
    broadcast_templates: list[BroadcastTemplate]
    live_timeline: list[TimelineItem]


class AdminIncidentLogRequest(BaseModel):
    incident_id: str
    actor_id: str
    note: str
    timestamp: str


class AdminIncidentLogResponse(BaseModel):
    success: bool
    log_id: str


class AdminIncidentResolveRequest(BaseModel):
    incident_id: str
    resolved_by: str
    resolution_note: str
    timestamp: str


class AdminIncidentResolveResponse(BaseModel):
    success: bool
    resolved_at: str


class UpdateGuestStatusRequest(BaseModel):
    status: GuestAccountabilityStatus
    updated_by: str


class UpdateGuestStatusResponse(BaseModel):
    success: bool
    guest_id: str
    status: GuestAccountabilityStatus


__all__ = [
    "AdminIncidentDetailResponse",
    "AdminIncidentLocation",
    "AdminIncidentLogRequest",
    "AdminIncidentLogResponse",
    "AdminIncidentResolveRequest",
    "AdminIncidentResolveResponse",
    "BroadcastRequest",
    "BroadcastResponse",
    "UpdateGuestStatusRequest",
    "UpdateGuestStatusResponse",
]
