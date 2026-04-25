"""
app/schemas/admin/map.py
"""

from typing import Literal

from pydantic import BaseModel

from app.core.constants import (
    BroadcastAudience,
    CrisisPriority,
    IncidentPinType,
    StaffDirectoryStatus,
)


class MapSummary(BaseModel):
    staff_online: int
    guests_present: int
    active_incidents: int
    live_feed_syncing: bool


class StaffLocation(BaseModel):
    employee_id: str
    lat: float
    lng: float
    floor: int
    status: Literal[
        StaffDirectoryStatus.AVAILABLE,
        StaffDirectoryStatus.RESPONDING,
        StaffDirectoryStatus.UNRESPONSIVE,
    ]


class GuestHeatmapPoint(BaseModel):
    zone_id: str
    lat: float
    lng: float
    count: int


class ActiveIncidentMapPoint(BaseModel):
    incident_id: str
    lat: float
    lng: float
    type: IncidentPinType
    severity: CrisisPriority


class CCTVCameraPoint(BaseModel):
    camera_id: str
    lat: float
    lng: float
    floor: int
    stream_url: str | None = None
    status: Literal["active", "offline"]


class MapLayers(BaseModel):
    staff_locations: list[StaffLocation]
    guest_heatmap: list[GuestHeatmapPoint]
    active_incidents: list[ActiveIncidentMapPoint]
    cctv_cameras: list[CCTVCameraPoint]


class IncidentCardLocation(BaseModel):
    floor: int
    room: str
    sector: str


class ClosestStaff(BaseModel):
    name: str
    role: str


class DispatchedUnit(BaseModel):
    employee_id: str
    name: str
    avatar_url: str | None = None
    status: Literal["en_route", "on_scene"]
    eta_seconds: int | None = None


class ActiveIncidentCard(BaseModel):
    incident_id: str
    title: str
    incident_code: str
    auto_triggered: bool
    elapsed_seconds: int
    location: IncidentCardLocation
    sensor_status: Literal["active", "inactive"]
    proximity_guests: int
    closest_staff: ClosestStaff
    dispatched_units: list[DispatchedUnit]


class AdminMapDataResponse(BaseModel):
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
    new_severity: CrisisPriority


class BroadcastRequest(BaseModel):
    incident_id: str
    audience: BroadcastAudience
    room_id: str | None = None
    message: str
    channels: list[Literal["app_push", "whatsapp", "sms"]]
    sent_by: str


class BroadcastResponse(BaseModel):
    success: bool
    broadcast_id: str
    recipients: int
