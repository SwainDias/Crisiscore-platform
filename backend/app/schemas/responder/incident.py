"""
app/schemas/responder/incident.py
"""

from pydantic import BaseModel

from app.core.constants import IncidentStatus, IncidentType, ResponderUnitStatus, SOPStepStatus


class GeoCoordinates(BaseModel):
    lat: float
    lng: float


class IncidentLocation(BaseModel):
    sector: str
    area_name: str
    coordinates: GeoCoordinates


class ActiveResponder(BaseModel):
    responder_id: str
    unit_label: str
    name: str
    status: ResponderUnitStatus
    eta_seconds: int | None = None


class SOPStep(BaseModel):
    step_id: str
    order: int
    title: str
    description: str | None = None
    status: SOPStepStatus
    completed_at: str | None = None


class SOPSummary(BaseModel):
    protocol_name: str
    total_steps: int
    completed_steps: int
    steps: list[SOPStep]


class ResponderIncidentResponse(BaseModel):
    incident_id: str
    incident_code: str
    type: IncidentType
    status: IncidentStatus
    title: str
    description: str
    location: IncidentLocation
    elapsed_seconds: int
    started_at: str
    active_responders: list[ActiveResponder]
    sop: SOPSummary


class BackupRequestResponse(BaseModel):
    success: bool
    backup_request_id: str


class LogUpdateRequest(BaseModel):
    incident_id: str
    responder_id: str
    note: str
    timestamp: str


class LogUpdateResponse(BaseModel):
    success: bool
    log_id: str


class ResolveRequest(BaseModel):
    incident_id: str
    resolved_by: str
    resolution_note: str
    timestamp: str


class ResolveResponse(BaseModel):
    success: bool
    resolved_at: str
