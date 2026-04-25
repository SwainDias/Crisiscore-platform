"""
app/services/admin_incident_service.py
"""

import uuid
from datetime import UTC, datetime

from app.core.constants import (
    CrisisPriority,
    ExternalService,
    ExternalServiceStatus,
    GuestAccountabilityStatus,
    IncidentStatus,
)
from app.core.exceptions import NotFoundException
from app.db.repositories.admin_repository import (
    BroadcastRepository,
    IncidentLogRepository,
    PropertyRepository,
    ResponderAssignmentRepository,
    StaffDirectoryRepository,
)
from app.db.repositories.guest_repository import GuestRepository
from app.db.repositories.incident_command_repository import IncidentCommandRepository
from app.schemas.admin.incident import (
    AdminIncidentDetailResponse,
    AdminIncidentLocation,
    AdminIncidentLogRequest,
    AdminIncidentLogResponse,
    AdminIncidentResolveRequest,
    AdminIncidentResolveResponse,
    BroadcastTemplate,
    ExternalServiceItem,
    GuestAccountabilityItem,
    ResponderAssignment,
    ResponderPin,
    SweepZone,
    TacticalMap,
    TimelineItem,
    UpdateGuestStatusRequest,
    UpdateGuestStatusResponse,
)
from app.schemas.admin.map import (
    AssignResponderRequest,
    AssignResponderResponse,
    BroadcastRequest,
    BroadcastResponse,
    EscalateRequest,
    EscalateResponse,
)


class AdminIncidentService:
    def __init__(
        self,
        incident_repo: IncidentCommandRepository,
        staff_repo: StaffDirectoryRepository,
        guest_repo: GuestRepository,
        property_repo: PropertyRepository,
        assignment_repo: ResponderAssignmentRepository,
        log_repo: IncidentLogRepository,
        broadcast_repo: BroadcastRepository,
    ) -> None:
        self._incident_repo = incident_repo
        self._staff_repo = staff_repo
        self._guest_repo = guest_repo
        self._property_repo = property_repo
        self._assignment_repo = assignment_repo
        self._log_repo = log_repo
        self._broadcast_repo = broadcast_repo

    async def get_incident(self, incident_id: str) -> AdminIncidentDetailResponse:
        incident = await self._incident_repo.get_by_incident_id(incident_id)
        if not incident:
            raise NotFoundException(message=f"Incident '{incident_id}' not found.")

        property_doc = await self._property_repo.get_by_property_id(incident.get("property_id", ""))
        location = incident.get("location", {})

        responders = self._to_assignments(incident.get("responder_assignments", []))
        guest_accountability = await self._guest_accountability(incident)
        timeline = await self._timeline(incident)

        responders_on_scene = len([r for r in responders if r.status == "on_scene"])
        guests_unaccounted = len(
            [g for g in guest_accountability if g.status == GuestAccountabilityStatus.UNKNOWN]
        )

        return AdminIncidentDetailResponse(
            incident_id=incident.get("incident_id", incident_id),
            event_code=incident.get("event_code", incident.get("incident_code", "EVT-UNKNOWN")),
            severity=self._to_priority(incident.get("severity")),
            status=incident.get("status", IncidentStatus.ACTIVE),
            type=incident.get("type", "custom"),
            title=incident.get("title", "Incident"),
            location=AdminIncidentLocation(
                property=(property_doc or {}).get("name", "Property"),
                building=location.get("building", "Main Building"),
                zone=location.get("zone", location.get("sector", "Unknown")),
                floor=int(location.get("floor", 0)),
            ),
            elapsed_seconds=self._elapsed_seconds(incident),
            responders_on_scene=responders_on_scene,
            guests_unaccounted=guests_unaccounted,
            services_notified=incident.get("services_notified", ["fire", "medical"]),
            sop_progress_percent=self._sop_progress(incident.get("sop", {})),
            tactical_map=self._tactical_map(location, responders),
            responder_assignments=responders,
            guest_accountability=guest_accountability,
            external_services=self._external_services(incident.get("external_services", [])),
            broadcast_templates=self._broadcast_templates(),
            live_timeline=timeline,
        )

    async def log_update(self, incident_id: str, request: AdminIncidentLogRequest) -> AdminIncidentLogResponse:
        incident = await self._incident_repo.get_by_incident_id(incident_id)
        if not incident:
            raise NotFoundException(message=f"Incident '{incident_id}' not found.")

        log_id = str(uuid.uuid4())
        await self._incident_repo.append_log(
            incident_id,
            {
                "event_id": log_id,
                "timestamp": request.timestamp,
                "title": "Admin update",
                "description": request.note,
                "icon_type": "check",
            },
        )
        await self._log_repo.create_log(
            incident_id,
            {
                "log_id": log_id,
                "actor_id": request.actor_id,
                "note": request.note,
                "timestamp": request.timestamp,
            },
        )

        return AdminIncidentLogResponse(success=True, log_id=log_id)

    async def escalate(self, request: EscalateRequest) -> EscalateResponse:
        incident = await self._incident_repo.get_by_incident_id(request.incident_id)
        if not incident:
            raise NotFoundException(message=f"Incident '{request.incident_id}' not found.")

        new_priority = self._next_priority(incident.get("severity"))
        await self._incident_repo.set_severity(
            incident_id=request.incident_id,
            severity=new_priority.value,
            escalated_by=request.escalated_by,
            reason=request.reason,
            timestamp=datetime.now(UTC),
        )
        return EscalateResponse(success=True, new_severity=new_priority)

    async def resolve(
        self,
        incident_id: str,
        request: AdminIncidentResolveRequest,
    ) -> AdminIncidentResolveResponse:
        incident = await self._incident_repo.get_by_incident_id(incident_id)
        if not incident:
            raise NotFoundException(message=f"Incident '{incident_id}' not found.")

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
                "note": f"Resolved: {request.resolution_note}",
                "timestamp": request.timestamp,
            },
        )

        return AdminIncidentResolveResponse(success=True, resolved_at=resolved_at.isoformat())

    async def assign_responder(self, request: AssignResponderRequest) -> AssignResponderResponse:
        incident = await self._incident_repo.get_by_incident_id(request.incident_id)
        if not incident:
            raise NotFoundException(message=f"Incident '{request.incident_id}' not found.")

        staff = await self._staff_repo.get_by_employee_id(request.employee_id)
        if not staff:
            raise NotFoundException(message=f"Employee '{request.employee_id}' not found.")

        assignment_id = str(uuid.uuid4())
        await self._assignment_repo.insert_one(
            {
                "assignment_id": assignment_id,
                "incident_id": request.incident_id,
                "employee_id": request.employee_id,
                "assigned_by": request.assigned_by,
                "status": "en_route",
                "eta_seconds": 180,
            }
        )

        await self._incident_repo.upsert_responder_assignment(
            request.incident_id,
            request.employee_id,
            {
                "name": staff.get("name", ""),
                "role": staff.get("role", "responder"),
                "team": staff.get("team"),
                "status": "en_route",
                "eta_seconds": 180,
            },
        )

        return AssignResponderResponse(success=True, assignment_id=assignment_id)

    async def update_guest_status(
        self,
        incident_id: str,
        guest_id: str,
        request: UpdateGuestStatusRequest,
    ) -> UpdateGuestStatusResponse:
        incident = await self._incident_repo.get_by_incident_id(incident_id)
        if not incident:
            raise NotFoundException(message=f"Incident '{incident_id}' not found.")

        guest = await self._guest_repo.get_by_guest_id(guest_id)
        if not guest:
            raise NotFoundException(message=f"Guest '{guest_id}' not found.")

        await self._incident_repo.upsert_guest_status(
            incident_id,
            guest_id,
            {
                "room": guest.get("room_number") or guest.get("room_id", ""),
                "name": guest.get("name", "Guest"),
                "status": request.status,
            },
        )

        await self._log_repo.create_log(
            incident_id,
            {
                "log_id": str(uuid.uuid4()),
                "actor_id": request.updated_by,
                "note": f"Guest {guest_id} marked as {request.status}",
                "timestamp": datetime.now(UTC).isoformat(),
            },
        )

        return UpdateGuestStatusResponse(success=True, guest_id=guest_id, status=request.status)

    async def broadcast(self, request: BroadcastRequest, property_id: str | None = None) -> BroadcastResponse:
        property_doc = await self._resolve_property(property_id)
        pid = property_doc["property_id"]

        incident = await self._incident_repo.get_by_incident_id(request.incident_id)
        floor = None
        if incident:
            floor = (incident.get("location") or {}).get("floor")

        recipients = await self._broadcast_repo.count_recipients_for_audience(
            property_id=pid,
            audience=request.audience,
            room_id=request.room_id,
            floor=floor,
            guest_repo=self._guest_repo,
        )

        broadcast_id = str(uuid.uuid4())
        await self._broadcast_repo.insert_one(
            {
                "broadcast_id": broadcast_id,
                "property_id": pid,
                "incident_id": request.incident_id,
                "audience": request.audience,
                "room_id": request.room_id,
                "message": request.message,
                "channels": request.channels,
                "sent_by": request.sent_by,
                "recipients": recipients,
            }
        )

        return BroadcastResponse(success=True, broadcast_id=broadcast_id, recipients=recipients)

    async def _resolve_property(self, property_id: str | None) -> dict:
        property_doc = None
        if property_id:
            property_doc = await self._property_repo.get_by_property_id(property_id)
        if not property_doc:
            property_doc = await self._property_repo.get_default()
        if not property_doc:
            property_doc = {"property_id": "PROP-DEFAULT", "name": "Rapid Response Property"}
        return property_doc

    def _to_assignments(self, rows: list[dict]) -> list[ResponderAssignment]:
        return [
            ResponderAssignment(
                employee_id=row.get("employee_id", ""),
                name=row.get("name", "Responder"),
                role=row.get("role", "responder"),
                team=row.get("team"),
                status=row.get("status", "standby"),
                eta_seconds=row.get("eta_seconds"),
            )
            for row in rows
        ]

    async def _guest_accountability(self, incident: dict) -> list[GuestAccountabilityItem]:
        existing = incident.get("guest_accountability", [])
        if existing:
            return [
                GuestAccountabilityItem(
                    guest_id=row.get("guest_id", ""),
                    room=row.get("room", ""),
                    name=row.get("name", "Guest"),
                    status=row.get("status", GuestAccountabilityStatus.UNKNOWN),
                )
                for row in existing
            ]

        guests = await self._guest_repo.list_for_property(incident.get("property_id", ""), limit=200)
        return [
            GuestAccountabilityItem(
                guest_id=g.get("guest_id", ""),
                room=g.get("room_number", g.get("room_id", "")),
                name=g.get("name", "Guest"),
                status=GuestAccountabilityStatus.UNKNOWN,
            )
            for g in guests
        ]

    async def _timeline(self, incident: dict) -> list[TimelineItem]:
        timeline_raw = incident.get("timeline", [])
        logs = await self._log_repo.list_for_incident(incident.get("incident_id", ""), limit=100)

        timeline: list[TimelineItem] = [
            TimelineItem(
                event_id=row.get("event_id", str(uuid.uuid4())),
                timestamp=str(row.get("timestamp", datetime.now(UTC).isoformat())),
                description=row.get("description", row.get("title", "Update")),
                icon=row.get("icon_type", "check"),
            )
            for row in timeline_raw
        ]
        timeline.extend(
            [
                TimelineItem(
                    event_id=row.get("log_id", str(uuid.uuid4())),
                    timestamp=str(row.get("timestamp", datetime.now(UTC).isoformat())),
                    description=row.get("note", "Update"),
                    icon="check",
                )
                for row in logs
            ]
        )
        timeline.sort(key=lambda item: item.timestamp)
        return timeline

    @staticmethod
    def _external_services(rows: list[dict]) -> list[ExternalServiceItem]:
        if not rows:
            return [
                ExternalServiceItem(service=ExternalService.FIRE_DEPARTMENT, status=ExternalServiceStatus.EN_ROUTE),
                ExternalServiceItem(service=ExternalService.MEDICAL, status=ExternalServiceStatus.STANDBY),
            ]
        return [
            ExternalServiceItem(
                service=row.get("service", ExternalService.MEDICAL),
                status=row.get("status", ExternalServiceStatus.NOT_NOTIFIED),
                eta_seconds=row.get("eta_seconds"),
            )
            for row in rows
        ]

    @staticmethod
    def _broadcast_templates() -> list[BroadcastTemplate]:
        return [
            BroadcastTemplate(
                template_id="tmpl-evacuate",
                label="Evacuation Notice",
                body="Please evacuate immediately using the nearest emergency staircase.",
            ),
            BroadcastTemplate(
                template_id="tmpl-shelter",
                label="Shelter-in-Place",
                body="Remain in your room, lock doors, and await further updates.",
            ),
        ]

    @staticmethod
    def _to_priority(raw: str | None) -> CrisisPriority:
        if raw in (CrisisPriority.P1, CrisisPriority.P2, CrisisPriority.P3):
            return CrisisPriority(raw)
        if raw == "critical":
            return CrisisPriority.P1
        if raw == "warning":
            return CrisisPriority.P2
        return CrisisPriority.P3

    @staticmethod
    def _next_priority(raw: str | None) -> CrisisPriority:
        current = AdminIncidentService._to_priority(raw)
        if current == CrisisPriority.P3:
            return CrisisPriority.P2
        return CrisisPriority.P1

    @staticmethod
    def _sop_progress(sop: dict) -> float:
        if not sop:
            return 0.0
        completed = sop.get("completed_steps")
        total = sop.get("total_steps")
        if isinstance(completed, int) and isinstance(total, int) and total > 0:
            return round((completed / total) * 100, 2)

        steps = sop.get("steps", [])
        if not steps:
            return 0.0
        done = len([s for s in steps if s.get("status") == "completed"])
        return round((done / len(steps)) * 100, 2)

    @staticmethod
    def _tactical_map(location: dict, responders: list[ResponderAssignment]) -> TacticalMap:
        lat = float((location.get("coordinates") or {}).get("lat", 0.0))
        lng = float((location.get("coordinates") or {}).get("lng", 0.0))
        floor = int(location.get("floor", 0))
        return TacticalMap(
            floor=floor,
            responder_pins=[
                ResponderPin(
                    label=r.name,
                    lat=lat + idx * 0.0001,
                    lng=lng + idx * 0.0001,
                )
                for idx, r in enumerate(responders)
            ],
            incident_pin=ResponderPin(label="Incident", lat=lat, lng=lng),
            sweep_zones=[
                SweepZone(
                    zone_id=f"zone-{floor}-1",
                    label=f"Floor {floor} Sector A",
                    lat=lat,
                    lng=lng,
                    width=0.0004,
                    height=0.0003,
                )
            ],
        )

    @staticmethod
    def _elapsed_seconds(incident: dict) -> int:
        started = AdminIncidentService._to_datetime(
            incident.get("started_at") or incident.get("created_at")
        )
        return max(int((datetime.now(UTC) - started).total_seconds()), 0)

    @staticmethod
    def _to_datetime(value: object | None) -> datetime:
        if isinstance(value, datetime):
            return value if value.tzinfo else value.replace(tzinfo=UTC)
        if isinstance(value, str):
            parsed = datetime.fromisoformat(value)
            return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)
        return datetime.now(UTC)
