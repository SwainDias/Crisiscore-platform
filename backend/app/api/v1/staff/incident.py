"""
app/api/v1/staff/incident.py
GET  /api/v1/staff/incident/{incident_id}/summary
POST /api/v1/staff/incident/{incident_id}/action-item
GET  /api/v1/staff/incident/{incident_id}/report/export
"""

from fastapi import APIRouter, Depends

from app.core.dependencies import CurrentStaff, DBDep
from app.db.repositories.action_item_repository import ActionItemRepository
from app.db.repositories.incident_repository import IncidentRepository
from app.schemas.staff.incident import (
    ExportReportResponse,
    IncidentSummaryResponse,
    LogActionItemRequest,
    LogActionItemResponse,
)
from app.services.incident_service import IncidentService

router = APIRouter(prefix="/staff/incident", tags=["Staff — Incident"])


def _get_service(db: DBDep) -> IncidentService:
    return IncidentService(IncidentRepository(db), ActionItemRepository(db))


@router.get(
    "/{incident_id}/summary",
    response_model=IncidentSummaryResponse,
    summary="Post-Incident Summary",
    description=(
        "Returns the full post-incident report for a resolved incident: KPIs, "
        "event timeline, and improvement opportunities."
    ),
)
async def get_incident_summary(
    incident_id: str,
    current_staff: CurrentStaff,
    service: IncidentService = Depends(_get_service),
) -> IncidentSummaryResponse:
    return await service.get_summary(incident_id)


@router.post(
    "/{incident_id}/action-item",
    response_model=LogActionItemResponse,
    summary="Log Action Item",
    description=(
        "Creates an action item linked to an improvement opportunity from the "
        "post-incident review. Assigns it to a staff member for follow-up."
    ),
)
async def log_action_item(
    incident_id: str,
    payload: LogActionItemRequest,
    current_staff: CurrentStaff,
    service: IncidentService = Depends(_get_service),
) -> LogActionItemResponse:
    return await service.log_action_item(incident_id, payload)


@router.get(
    "/{incident_id}/report/export",
    response_model=ExportReportResponse,
    summary="Export Incident Report",
    description=(
        "Generates a signed, time-limited URL for downloading the full incident "
        "PDF report. URL expires after the configured window."
    ),
)
async def export_report(
    incident_id: str,
    current_staff: CurrentStaff,
    service: IncidentService = Depends(_get_service),
) -> ExportReportResponse:
    return await service.export_report(incident_id)
