"""
app/schemas/staff/home.py
"""

from pydantic import BaseModel

from app.core.constants import (
    DutyStatus,
    IncidentSeverity,
    TaskPriority,
    TaskStatus,
)


class StaffSummary(BaseModel):
    employee_id: str
    name: str
    avatar_url: str | None = None


class ActiveIncident(BaseModel):
    present: bool
    incident_id: str | None = None
    title: str | None = None
    body: str | None = None
    severity: IncidentSeverity | None = None
    cta_route: str | None = None


class Assignment(BaseModel):
    assignment_id: str
    label: str


class MyStatus(BaseModel):
    duty_status: DutyStatus
    assignment: Assignment
    checkin_time: str
    vehicle: str | None = None


class LiveMap(BaseModel):
    active_zones: int
    units_deployed: int
    map_preview_url: str | None = None
    route: str


class TaskItem(BaseModel):
    task_id: str
    title: str
    priority: TaskPriority
    status: TaskStatus
    due_at: str | None = None


class HistoryLog(BaseModel):
    log_id: str
    timestamp: str
    summary: str


class StaffHomeResponse(BaseModel):
    staff: StaffSummary
    active_incident: ActiveIncident
    my_status: MyStatus
    sos_enabled: bool
    live_map: LiveMap
    my_tasks: list[TaskItem]
    tasks_total: int
    history: list[HistoryLog]


# ─── SOS ─────────────────────────────────────────────────────────────────────

class SOSTriggerLocation(BaseModel):
    lat: float
    lng: float


class SOSTriggerRequest(BaseModel):
    employee_id: str
    location: SOSTriggerLocation
    timestamp: str


class SOSTriggerResponse(BaseModel):
    broadcast_id: str
    acknowledged: bool
