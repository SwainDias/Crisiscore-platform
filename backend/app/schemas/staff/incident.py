"""
app/schemas/staff/incident.py
"""

from pydantic import BaseModel

from app.core.constants import IncidentStatus, TimelineIconType


class IncidentKPIs(BaseModel):
    response_time_seconds: int
    sla_delta_seconds: int
    personnel_accounted: int
    personnel_total: int
    sop_compliance_percent: float
    deviations_logged: int


class TimelineEvent(BaseModel):
    event_id: str
    timestamp: str
    title: str
    description: str
    icon_type: TimelineIconType


class ImprovementOpportunity(BaseModel):
    opp_id: str
    title: str
    description: str
    action_logged: bool


class IncidentSummaryResponse(BaseModel):
    incident_id: str
    event_code: str
    title: str
    status: IncidentStatus
    concluded_at: str
    kpis: IncidentKPIs
    timeline: list[TimelineEvent]
    improvement_opportunities: list[ImprovementOpportunity]


class LogActionItemRequest(BaseModel):
    opp_id: str
    note: str
    assigned_to: str | None = None
    logged_by: str
    timestamp: str


class LogActionItemResponse(BaseModel):
    success: bool
    action_item_id: str


class ExportReportResponse(BaseModel):
    report_url: str
    expires_at: str
