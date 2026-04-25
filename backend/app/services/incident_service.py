"""
app/services/incident_service.py
Business logic for post-incident summary, action items, and report export.
"""

import uuid
from datetime import UTC, datetime, timedelta

from app.core.config import get_settings
from app.core.exceptions import NotFoundException
from app.db.repositories.action_item_repository import ActionItemRepository
from app.db.repositories.incident_repository import IncidentRepository
from app.schemas.staff.incident import (
    ExportReportResponse,
    ImprovementOpportunity,
    IncidentKPIs,
    IncidentSummaryResponse,
    LogActionItemRequest,
    LogActionItemResponse,
    TimelineEvent,
)

settings = get_settings()


class IncidentService:
    def __init__(
        self,
        incident_repo: IncidentRepository,
        action_item_repo: ActionItemRepository,
    ) -> None:
        self._incident_repo = incident_repo
        self._action_item_repo = action_item_repo

    async def get_summary(self, incident_id: str) -> IncidentSummaryResponse:
        doc = await self._incident_repo.get_resolved_by_id(incident_id)
        if not doc:
            raise NotFoundException(message=f"Resolved incident '{incident_id}' not found.")

        action_items = await self._action_item_repo.list_for_incident(incident_id)
        logged_opp_ids = {ai["opp_id"] for ai in action_items}

        raw_opps = doc.get("improvement_opportunities", [])
        opportunities = [
            ImprovementOpportunity(
                opp_id=opp["opp_id"],
                title=opp["title"],
                description=opp["description"],
                action_logged=opp["opp_id"] in logged_opp_ids,
            )
            for opp in raw_opps
        ]

        timeline = [
            TimelineEvent(
                event_id=evt.get("event_id", str(uuid.uuid4())),
                timestamp=self._to_iso(evt.get("timestamp")),
                title=evt["title"],
                description=evt["description"],
                icon_type=evt.get("icon_type", "check"),
            )
            for evt in doc.get("timeline", [])
        ]

        kpi_raw = doc.get("kpis", {})
        kpis = IncidentKPIs(
            response_time_seconds=kpi_raw.get("response_time_seconds", 0),
            sla_delta_seconds=kpi_raw.get("sla_delta_seconds", 0),
            personnel_accounted=kpi_raw.get("personnel_accounted", 0),
            personnel_total=kpi_raw.get("personnel_total", 0),
            sop_compliance_percent=kpi_raw.get("sop_compliance_percent", 0.0),
            deviations_logged=kpi_raw.get("deviations_logged", 0),
        )

        return IncidentSummaryResponse(
            incident_id=incident_id,
            event_code=doc.get("event_code", "EVT-UNKNOWN"),
            title=doc.get("title", "Incident"),
            status=doc["status"],
            concluded_at=self._to_iso(doc.get("concluded_at")),
            kpis=kpis,
            timeline=timeline,
            improvement_opportunities=opportunities,
        )

    async def log_action_item(
        self, incident_id: str, request: LogActionItemRequest
    ) -> LogActionItemResponse:
        # Verify incident exists
        doc = await self._incident_repo.get_resolved_by_id(incident_id)
        if not doc:
            raise NotFoundException(message=f"Incident '{incident_id}' not found.")

        action_item_id = str(uuid.uuid4())
        await self._action_item_repo.insert_one(
            {
                "action_item_id": action_item_id,
                "incident_id": incident_id,
                "opp_id": request.opp_id,
                "note": request.note,
                "assigned_to": request.assigned_to,
                "logged_by": request.logged_by,
                "logged_at": datetime.fromisoformat(request.timestamp),
            }
        )

        return LogActionItemResponse(success=True, action_item_id=action_item_id)

    async def export_report(self, incident_id: str) -> ExportReportResponse:
        doc = await self._incident_repo.get_resolved_by_id(incident_id)
        if not doc:
            raise NotFoundException(message=f"Incident '{incident_id}' not found.")

        expires_at = (
            datetime.now(UTC) + timedelta(hours=settings.report_export_expiry_hours)
        ).isoformat()

        report_url = f"{settings.report_export_base_url}/{incident_id}/report.pdf"
        return ExportReportResponse(report_url=report_url, expires_at=expires_at)

    # ─── Helpers ─────────────────────────────────────────────────────────────

    @staticmethod
    def _to_iso(value) -> str:
        if value is None:
            return datetime.now(UTC).isoformat()
        if isinstance(value, datetime):
            return value.isoformat()
        return str(value)
