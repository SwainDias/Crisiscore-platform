"""
app/schemas/responder/responder.py
Pydantic models for responder incident dashboard.
"""

from pydantic import BaseModel

from app.core.constants import (
    IncidentContainmentStatus,
    IncidentType,
    ResponderStatus,
    SOPStepStatus,
)


class IncidentLocation(BaseModel):
    sector: str
    area_name: str
    coordinates: dict[str, float]   # {"lat": ..., "lng": ...}


class ActiveResponder(BaseModel):
    responder_id: str
    unit_label: str
    name: str
    status: ResponderStatus
    eta_seconds: int | None = None


class SOPStep(BaseModel):
    step_id: str
    order: int
    title: str
    description: str | None = None
    status: SOPStepStatus
    completed_at: str | None = None


class SOPProgress(BaseModel):
    protocol_name: str
    total_steps: int
    completed_steps: int
    steps: list[SOPStep]


class ResponderIncidentResponse(BaseModel):
    incident_id: str
    incident_code: str
    type: IncidentType
    status: IncidentContainmentStatus
    title: str
    description: str
    location: IncidentLocation
    elapsed_seconds: int
    started_at: str
    active_responders: list[ActiveResponder]
    sop: SOPProgress


class LogUpdateRequest(BaseModel):
    incident_id: str
    responder_id: str
    note: str
    timestamp: str


class ResolveRequest(BaseModel):
    incident_id: str
    resolved_by: str
    resolution_note: str
    timestamp: str


class ResolveResponse(BaseModel):
    success: bool
    resolved_at: str


class BackupRequest(BaseModel):
    incident_id: str
    requested_by: str
    reason: str


class BackupResponse(BaseModel):
    success: bool
    backup_request_id: str