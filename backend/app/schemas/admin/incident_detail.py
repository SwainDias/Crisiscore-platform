"""
app/schemas/admin/incident_detail.py
"""

from pydantic import BaseModel

from app.core.constants import (
    ExternalService,
    ExternalServiceStatus,
    GuestAccountabilityStatus,
    IncidentContainmentStatus,
    IncidentPriority,
    IncidentType,
    ResponderStatus,
)


class IncidentLocationDetail(BaseModel):
    property: str
    building: str
    zone: str
    floor: int


class ResponderPin(BaseModel):
    label: str
    lat: float
    lng: float


class IncidentPinDetail(BaseModel):
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
    incident_pin: IncidentPinDetail
    sweep_zones: list[SweepZone]


class ResponderAssignment(BaseModel):
    employee_id: str
    name: str
    role: str
    team: str | None = None
    status: ResponderStatus
    eta_seconds: int | None = None


class GuestAccountabilityEntry(BaseModel):
    guest_id: str
    room: str
    name: str
    status: GuestAccountabilityStatus


class ExternalServiceEntry(BaseModel):
    service: ExternalService
    status: ExternalServiceStatus
    eta_seconds: int | None = None


class BroadcastTemplate(BaseModel):
    template_id: str
    label: str
    body: str


class LiveTimelineEvent(BaseModel):
    event_id: str
    timestamp: str
    description: str
    icon: str


class AdminIncidentDetailResponse(BaseModel):
    incident_id: str
    event_code: str
    severity: IncidentPriority
    status: IncidentContainmentStatus
    type: IncidentType
    title: str
    location: IncidentLocationDetail
    elapsed_seconds: int
    responders_on_scene: int
    guests_unaccounted: int
    services_notified: list[ExternalService]
    sop_progress_percent: float
    tactical_map: TacticalMap
    responder_assignments: list[ResponderAssignment]
    guest_accountability: list[GuestAccountabilityEntry]
    external_services: list[ExternalServiceEntry]
    broadcast_templates: list[BroadcastTemplate]
    live_timeline: list[LiveTimelineEvent]


class AdminLogUpdateRequest(BaseModel):
    incident_id: str
    responder_id: str
    note: str
    timestamp: str


class AdminResolveRequest(BaseModel):
    incident_id: str
    resolved_by: str
    resolution_note: str
    timestamp: str


class AdminResolveResponse(BaseModel):
    success: bool
    resolved_at: str


class UpdateGuestStatusRequest(BaseModel):
    status: GuestAccountabilityStatus
    updated_by: str