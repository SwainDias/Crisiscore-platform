"""
app/schemas/admin/overview.py
"""

from pydantic import BaseModel

from app.core.constants import CrisisPriority, IncidentPinType, IncidentQueueStatus, ResponderUnitStatus


class PropertySummary(BaseModel):
    property_id: str
    name: str
    server_time: str


class ActiveIncidentBanner(BaseModel):
    present: bool
    incident_id: str | None = None
    title: str | None = None
    severity: CrisisPriority | None = None
    responders_deployed: int | None = None
    guests_in_zone: int | None = None
    cta_route: str | None = None


class OverviewKPIs(BaseModel):
    staff_on_duty: int
    active_incidents: int
    guests_tracked: int
    avg_response_time_seconds: int


class IncidentPin(BaseModel):
    lat: float | None = None
    lng: float | None = None
    floor: int | None = None
    type: IncidentPinType | None = None


class LiveMapSummary(BaseModel):
    active_floor: int
    floors: list[int]
    incident_pin: IncidentPin


class ActiveResponderCard(BaseModel):
    employee_id: str
    name: str
    initials: str
    role: str
    status: ResponderUnitStatus


class IncidentQueueItem(BaseModel):
    incident_id: str
    title: str
    location: str
    status: IncidentQueueStatus
    age_seconds: int


class AdminOverviewResponse(BaseModel):
    property: PropertySummary
    active_incident_banner: ActiveIncidentBanner
    kpis: OverviewKPIs
    live_map_summary: LiveMapSummary
    active_responders: list[ActiveResponderCard]
    incident_queue: list[IncidentQueueItem]
