"""
app/services/responder_incident_service.py
Business logic for the first-responder incident command screen.
"""

import uuid
from datetime import UTC, datetime

from app.core.constants import IncidentContainmentStatus, IncidentStatus, SOPStepStatus
from app.core.exceptions import NotFoundException
from app.db.repositories.incident_repository import IncidentRepository
from app.db.repositories.responder_repository import (
    ResponderLogRepository,
    SOPRepository,
)
from app.schemas.responder.responder import (
    ActiveResponder,
    BackupRequest,
    BackupResponse,
    LogUpdateRequest,
    ResolveRequest,
    ResolveResponse,
    ResponderIncidentResponse,
    SOPProgress,
    SOPStep,
)


class ResponderIncidentService:
    def __init__(
        self,
        incident_repo: IncidentRepository,
        log_repo: ResponderLogRepository,
        sop_repo: SOPRepository,
    ) -> None:
        self._incident_repo = incident_repo
        self._log_repo = log_repo
        self._sop_repo = sop_repo

    async def get_incident(self, incident_id: str) -> ResponderIncidentResponse:
        doc = await self._incident_repo.get_by_id(incident_id)
        if not doc:
            raise NotFoundException(message=f"Incident '{incident_id}' not found.")

        sop = await self._build_sop(doc.get("type", "fire"))
        responders = self._build_responders(doc.get("responder_assignments", []))

        started_at = doc.get("created_at", datetime.now(UTC))
        elapsed = int(
            (datetime.now(UTC) - started_at.replace(tzinfo=UTC)).total_seconds()
            if isinstance(started_at, datetime)
            else 0
        )

        return ResponderIncidentResponse(
            incident_id=incident_id,
            incident_code=doc.get("event_code", "EVT-UNKNOWN"),
            type=doc.get("type", "custom"),
            status=doc.get("status", IncidentContainmentStatus.ACTIVE),
            title=doc.get("title", ""),
            description=doc.get("description", ""),
            location={
                "sector": doc.get("sector", ""),
                "area_name": doc.get("area_name", ""),
                "coordinates": doc.get("coordinates", {"lat": 0.0, "lng": 0.0}),
            },
            elapsed_seconds=elapsed,
            started_at=(
                started_at.isoformat()
                if isinstance(started_at, datetime)
                else str(started_at)
            ),
            active_responders=responders,
            sop=sop,
        )

    async def log_update(self, request: LogUpdateRequest) -> dict:
        doc = await self._incident_repo.get_by_id(request.incident_id)
        if not doc:
            raise NotFoundException(message="Incident not found.")

        log_id = await self._log_repo.append_log(
            incident_id=request.incident_id,
            responder_id=request.responder_id,
            note=request.note,
            timestamp=datetime.fromisoformat(request.timestamp),
        )
        return {"success": True, "log_id": log_id}

    async def resolve_incident(self, request: ResolveRequest) -> ResolveResponse:
        doc = await self._incident_repo.get_by_id(request.incident_id)
        if not doc:
            raise NotFoundException(message="Incident not found.")

        resolved_at = datetime.fromisoformat(request.timestamp)
        await self._incident_repo.update_one(
            {"_id": doc.get("_id")},
            {
                "$set": {
                    "status": IncidentStatus.RESOLVED,
                    "concluded_at": resolved_at,
                    "resolved_by": request.resolved_by,
                    "resolution_note": request.resolution_note,
                }
            },
        )
        return ResolveResponse(success=True, resolved_at=resolved_at.isoformat())

    async def request_backup(self, request: BackupRequest) -> BackupResponse:
        backup_id = str(uuid.uuid4())
        # In production: fan out push notification to standby staff
        return BackupResponse(success=True, backup_request_id=backup_id)

    # ─── Helpers ─────────────────────────────────────────────────────────────

    async def _build_sop(self, incident_type: str) -> SOPProgress:
        protocol = await self._sop_repo.get_for_incident_type(incident_type)
        if not protocol:
            return SOPProgress(
                protocol_name="Standard Protocol",
                total_steps=0,
                completed_steps=0,
                steps=[],
            )

        raw_steps = protocol.get("steps", [])
        steps = [
            SOPStep(
                step_id=s.get("step_id", str(i)),
                order=i + 1,
                title=s["title"],
                description=s.get("description"),
                status=s.get("status", SOPStepStatus.PENDING),
                completed_at=s.get("completed_at"),
            )
            for i, s in enumerate(raw_steps)
        ]
        completed = sum(1 for s in steps if s.status == SOPStepStatus.COMPLETED)

        return SOPProgress(
            protocol_name=protocol.get("name", "Standard Protocol"),
            total_steps=len(steps),
            completed_steps=completed,
            steps=steps,
        )

    def _build_responders(self, raw: list[dict]) -> list[ActiveResponder]:
        return [
            ActiveResponder(
                responder_id=r.get("employee_id", ""),
                unit_label=r.get("unit_label", "Unit"),
                name=r.get("name", ""),
                status=r.get("status", "standby"),
                eta_seconds=r.get("eta_seconds"),
            )
            for r in raw
        ]
