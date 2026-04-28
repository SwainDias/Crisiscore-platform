"""
app/services/responder_incident_service.py
"""

import uuid
from datetime import UTC, datetime

from app.core.constants import IncidentErrorCode, IncidentStatus, IncidentType, ResponderUnitStatus, SOPStepStatus
from app.core.exceptions import NotFoundException
from app.db.repositories.admin_repository import IncidentLogRepository
from app.db.repositories.incident_command_repository import IncidentCommandRepository
from app.schemas.responder.incident import (
    ActiveResponder,
    BackupRequestResponse,
    GeoCoordinates,
    IncidentLocation,
    LogUpdateRequest,
    LogUpdateResponse,
    ResolveRequest,
    ResolveResponse,
    ResponderIncidentResponse,
    SOPStep,
    SOPSummary,
)


class ResponderIncidentService:
    def __init__(
        self,
        incident_repo: IncidentCommandRepository,
        log_repo: IncidentLogRepository,
    ) -> None:
        self._incident_repo = incident_repo
        self._log_repo = log_repo

    async def get_incident(self, incident_id: str) -> ResponderIncidentResponse:
        incident = await self._incident_repo.get_by_incident_id(incident_id)
        if not incident:
            raise NotFoundException(
                code=IncidentErrorCode.INCIDENT_NOT_FOUND,
                message=f"Incident '{incident_id}' not found.",
            )

        started_at_raw = incident.get("started_at") or incident.get("created_at")
        started_at = self._to_datetime(started_at_raw)
        elapsed_seconds = max(int((datetime.now(UTC) - started_at).total_seconds()), 0)

        location_data = incident.get("location", {})
        responders = self._to_responders(incident.get("responder_assignments", []))
        sop = self._to_sop(incident.get("sop", {}))

        return ResponderIncidentResponse(
            incident_id=incident.get("incident_id", incident_id),
            incident_code=incident.get("incident_code", incident.get("event_code", "INC-UNKNOWN")),
            type=incident.get("type", IncidentType.CUSTOM),
            status=incident.get("status", IncidentStatus.ACTIVE),
            title=incident.get("title", "Incident"),
            description=incident.get("description", ""),
            location=IncidentLocation(
                sector=location_data.get("sector", "Unknown Sector"),
                area_name=location_data.get("area_name", "Unknown Area"),
                coordinates=GeoCoordinates(
                    lat=float(location_data.get("coordinates", {}).get("lat", 0.0)),
                    lng=float(location_data.get("coordinates", {}).get("lng", 0.0)),
                ),
            ),
            elapsed_seconds=elapsed_seconds,
            started_at=started_at.isoformat(),
            active_responders=responders,
            sop=sop,
        )

    async def request_backup(self, incident_id: str, responder_id: str) -> BackupRequestResponse:
        incident = await self._incident_repo.get_by_incident_id(incident_id)
        if not incident:
            raise NotFoundException(
                code=IncidentErrorCode.INCIDENT_NOT_FOUND,
                message=f"Incident '{incident_id}' not found.",
            )

        backup_request_id = str(uuid.uuid4())
        timestamp = datetime.now(UTC).isoformat()
        await self._incident_repo.append_log(
            incident_id,
            {
                "event_id": backup_request_id,
                "timestamp": timestamp,
                "title": "Backup requested",
                "description": f"Responder {responder_id} requested additional support.",
                "icon_type": "alert",
            },
        )

        await self._log_repo.create_log(
            incident_id,
            {
                "log_id": backup_request_id,
                "actor_id": responder_id,
                "note": "Requested backup support",
                "timestamp": timestamp,
            },
        )

        return BackupRequestResponse(success=True, backup_request_id=backup_request_id)

    async def log_update(self, incident_id: str, request: LogUpdateRequest) -> LogUpdateResponse:
        incident = await self._incident_repo.get_by_incident_id(incident_id)
        if not incident:
            raise NotFoundException(
                code=IncidentErrorCode.INCIDENT_NOT_FOUND,
                message=f"Incident '{incident_id}' not found.",
            )

        log_id = str(uuid.uuid4())
        await self._incident_repo.append_log(
            incident_id,
            {
                "event_id": log_id,
                "timestamp": request.timestamp,
                "title": "Responder update",
                "description": request.note,
                "icon_type": "person",
            },
        )

        await self._log_repo.create_log(
            incident_id,
            {
                "log_id": log_id,
                "responder_id": request.responder_id,
                "note": request.note,
                "timestamp": request.timestamp,
            },
        )

        return LogUpdateResponse(success=True, log_id=log_id)

    async def resolve(self, incident_id: str, request: ResolveRequest) -> ResolveResponse:
        incident = await self._incident_repo.get_by_incident_id(incident_id)
        if not incident:
            raise NotFoundException(
                code=IncidentErrorCode.INCIDENT_NOT_FOUND,
                message=f"Incident '{incident_id}' not found.",
            )

        resolved_at = self._to_datetime(request.timestamp)
        await self._incident_repo.set_status(
            incident_id=incident_id,
            status=IncidentStatus.RESOLVED,
            timestamp=resolved_at,
            resolved_by=request.resolved_by,
            resolution_note=request.resolution_note,
        )

        await self._log_repo.create_log(
            incident_id,
            {
                "log_id": str(uuid.uuid4()),
                "actor_id": request.resolved_by,
                "note": f"Incident resolved: {request.resolution_note}",
                "timestamp": request.timestamp,
            },
        )

        return ResolveResponse(success=True, resolved_at=resolved_at.isoformat())

    @staticmethod
    def _to_responders(items: list[dict]) -> list[ActiveResponder]:
        responders: list[ActiveResponder] = []
        for row in items:
            responders.append(
                ActiveResponder(
                    responder_id=row.get("employee_id", "unknown"),
                    unit_label=row.get("unit_label", row.get("team", "Unit")),
                    name=row.get("name", "Responder"),
                    status=row.get("status", ResponderUnitStatus.DISPATCHED),
                    eta_seconds=row.get("eta_seconds"),
                )
            )
        return responders

    @staticmethod
    def _to_sop(raw: dict) -> SOPSummary:
        steps_raw = raw.get("steps", [])
        steps = [
            SOPStep(
                step_id=s.get("step_id", f"step-{idx + 1}"),
                order=int(s.get("order", idx + 1)),
                title=s.get("title", f"Step {idx + 1}"),
                description=s.get("description"),
                status=s.get("status", SOPStepStatus.PENDING),
                completed_at=s.get("completed_at"),
            )
            for idx, s in enumerate(steps_raw)
        ]

        completed_steps = sum(1 for s in steps if s.status == SOPStepStatus.COMPLETED)
        total_steps = raw.get("total_steps", len(steps))

        return SOPSummary(
            protocol_name=raw.get("protocol_name", "Standard Incident Response"),
            total_steps=total_steps,
            completed_steps=raw.get("completed_steps", completed_steps),
            steps=steps,
        )

    @staticmethod
    def _to_datetime(value: object | None) -> datetime:
        if isinstance(value, datetime):
            return value if value.tzinfo else value.replace(tzinfo=UTC)
        if isinstance(value, str):
            parsed = datetime.fromisoformat(value)
            return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)
        return datetime.now(UTC)
