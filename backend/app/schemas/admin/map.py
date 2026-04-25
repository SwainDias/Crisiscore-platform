"""
app/schemas/admin/map.py
"""

from pydantic import BaseModel

from app.core.constants import (
    IncidentPriority,
    IncidentType,
    StaffOperationalStatus,
)


class MapSummary(BaseModel):
    staff_online: int
    guests_present: int
    active_incidents: int
    live_feed_syncing: bool


class StaffLocationPin(BaseModel):
    employee_id: str
    lat: float
    lng: float
    floor: int
    status: StaffOperationalStatus


class GuestHeatmapZone(BaseModel):
    zone_id: str
    lat: float
    lng: float
    count: int


class IncidentMapPin(BaseModel):
    incident_id: str
    lat: float
    lng: float
    type: IncidentType
    severity: IncidentPriority


class CCTVCamera(BaseModel):
    camera_id: str
    lat: float
    lng: float
    floor: int
    stream_url: str | None = None
    status: str  # "active" | "offline"


class MapLayers(BaseModel):
    staff_locations: list[StaffLocationPin]
    guest_heatmap: list[GuestHeatmapZone]
    active_incidents: list[IncidentMapPin]
    cctv_cameras: list[CCTVCamera]


class DispatchedUnit(BaseModel):
    employee_id: str
    name: str
    avatar_url: str | None = None
    status: str
    eta_seconds: int | None = None


class ClosestStaff(BaseModel):
    name: str
    role: str


class ActiveIncidentCard(BaseModel):
    incident_id: str
    title: str
    incident_code: str
    auto_triggered: bool
    elapsed_seconds: int
    location: dict
    sensor_status: str
    proximity_guests: int
    closest_staff: ClosestStaff
    dispatched_units: list[DispatchedUnit]


class MapDataResponse(BaseModel):
    property_id: str
    floor: int
    floors_available: list[int]
    summary: MapSummary
    layers: MapLayers
    active_incident_card: ActiveIncidentCard | None = None


class AssignResponderRequest(BaseModel):
    incident_id: str
    employee_id: str
    assigned_by: str


class AssignResponderResponse(BaseModel):
    success: bool
    assignment_id: str


class EscalateRequest(BaseModel):
    incident_id: str
    reason: str
    escalated_by: str


class EscalateResponse(BaseModel):
    success: bool
    new_severity: IncidentPriority


class BroadcastRequest(BaseModel):
    incident_id: str
    audience: str  # all_guests | affected_floor | specific_room
    room_id: str | None = None
    message: str
    channels: list[str]
    sent_by: str


class BroadcastResponse(BaseModel):
    success: bool
    broadcast_id: str
    recipients: int
