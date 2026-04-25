"""
app/schemas/admin/overview.py
"""

from pydantic import BaseModel
from app.core.constants import (
    IncidentPriority,
    IncidentStatus,
    StaffOperationalStatus,
)


class PropertyInfo(BaseModel):
    property_id: str
    name: str
    server_time: str


class ActiveIncidentBanner(BaseModel):
    present: bool
    incident_id: str | None = None
    title: str | None = None
    severity: IncidentPriority | None = None
    responders_deployed: int | None = None
    guests_in_zone: int | None = None
    cta_route: str | None = None


class AdminKPIs(BaseModel):
    staff_on_duty: int
    active_incidents: int
    guests_tracked: int
    avg_response_time_seconds: int


class IncidentPin(BaseModel):
    lat: float | None = None
    lng: float | None = None
    floor: int | None = None
    type: str | None = None


class LiveMapSummary(BaseModel):
    active_floor: int
    floors: list[int]
    incident_pin: IncidentPin


class ActiveResponderCard(BaseModel):
    employee_id: str
    name: str
    initials: str
    role: str
    status: StaffOperationalStatus


class IncidentQueueItem(BaseModel):
    incident_id: str
    title: str
    location: str
    status: IncidentStatus
    age_seconds: int


class AdminOverviewResponse(BaseModel):
    property: PropertyInfo
    active_incident_banner: ActiveIncidentBanner
    kpis: AdminKPIs
    live_map_summary: LiveMapSummary
    active_responders: list[ActiveResponderCard]
    incident_queue: list[IncidentQueueItem]