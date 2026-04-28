"""
app/services/admin_map_service.py
"""

import uuid
from datetime import UTC, datetime

from app.core.constants import CrisisPriority, IncidentPinType, StaffDirectoryStatus
from app.core.exceptions import NotFoundException
from app.db.repositories.admin_repository import (
    BroadcastRepository,
    CCTVCameraRepository,
    PropertyRepository,
    ResponderAssignmentRepository,
    StaffDirectoryRepository,
)
from app.db.repositories.guest_repository import GuestRepository, RoomRepository
from app.db.repositories.incident_command_repository import IncidentCommandRepository
from app.schemas.admin.map import (
    ActiveIncidentCard,
    ActiveIncidentMapPoint,
    AdminMapDataResponse,
    AssignResponderRequest,
    AssignResponderResponse,
    BroadcastRequest,
    BroadcastResponse,
    ClosestStaff,
    CCTVCameraPoint,
    DispatchedUnit,
    EscalateRequest,
    EscalateResponse,
    GuestHeatmapPoint,
    IncidentCardLocation,
    MapLayers,
    MapSummary,
    StaffLocation,
)


class AdminMapService:
    def __init__(
        self,
        property_repo: PropertyRepository,
        incident_repo: IncidentCommandRepository,
        staff_repo: StaffDirectoryRepository,
        guest_repo: GuestRepository,
        room_repo: RoomRepository,
        camera_repo: CCTVCameraRepository,
        assignment_repo: ResponderAssignmentRepository,
        broadcast_repo: BroadcastRepository,
    ) -> None:
        self._property_repo = property_repo
        self._incident_repo = incident_repo
        self._staff_repo = staff_repo
        self._guest_repo = guest_repo
        self._room_repo = room_repo
        self._camera_repo = camera_repo
        self._assignment_repo = assignment_repo
        self._broadcast_repo = broadcast_repo

    async def get_map_data(self, floor: int | None, property_id: str | None = None) -> AdminMapDataResponse:
        property_doc = await self._resolve_property(property_id)
        pid = property_doc["property_id"]

        floors = await self._room_repo.list_floors(pid)
        incidents = await self._incident_repo.list_for_property(pid, include_resolved=False)
        lead_incident = incidents[0] if incidents else None

        selected_floor = floor
        if selected_floor is None:
            selected_floor = int((lead_incident or {}).get("location", {}).get("floor") or (floors[0] if floors else 0))

        staff_rows, _ = await self._staff_repo.list_staff(
            property_id=pid,
            role=None,
            status=None,
            floor=selected_floor,
            search=None,
            page=1,
            limit=200,
        )

        guest_rows = await self._guest_repo.list_for_property(pid, limit=1000)
        guest_rows = [g for g in guest_rows if int(g.get("floor", selected_floor)) == selected_floor]

        cameras = await self._camera_repo.list_for_floor(pid, selected_floor)

        layers = MapLayers(
            staff_locations=self._staff_locations(staff_rows, selected_floor),
            guest_heatmap=self._guest_heatmap(guest_rows),
            active_incidents=self._incident_points(incidents),
            cctv_cameras=[
                CCTVCameraPoint(
                    camera_id=c.get("camera_id", ""),
                    lat=float(c.get("lat", 0.0)),
                    lng=float(c.get("lng", 0.0)),
                    floor=int(c.get("floor", selected_floor)),
                    stream_url=c.get("stream_url"),
                    status=c.get("status", "offline"),
                )
                for c in cameras
            ],
        )

        return AdminMapDataResponse(
            property_id=pid,
            floor=selected_floor,
            floors_available=floors or [selected_floor],
            summary=MapSummary(
                staff_online=len([s for s in staff_rows if s.get("status") != StaffDirectoryStatus.OFF_DUTY]),
                guests_present=len(guest_rows),
                active_incidents=len(incidents),
                live_feed_syncing=True,
            ),
            layers=layers,
            active_incident_card=self._active_incident_card(lead_incident),
        )

    async def assign_responder(self, request: AssignResponderRequest) -> AssignResponderResponse:
        incident = await self._incident_repo.get_by_incident_id(request.incident_id)
        if not incident:
            raise NotFoundException(message=f"Incident '{request.incident_id}' not found.")

        staff = await self._staff_repo.get_by_employee_id(request.employee_id)
        if not staff:
            raise NotFoundException(message=f"Employee '{request.employee_id}' not found.")

        assignment_id = str(uuid.uuid4())
        assignment = {
            "assignment_id": assignment_id,
            "incident_id": request.incident_id,
            "employee_id": request.employee_id,
            "assigned_by": request.assigned_by,
            "status": "en_route",
            "eta_seconds": 180,
            "created_at": datetime.now(UTC),
        }
        await self._assignment_repo.insert_one(assignment)

        await self._incident_repo.upsert_responder_assignment(
            request.incident_id,
            request.employee_id,
            {
                "name": staff.get("name", ""),
                "role": staff.get("role", "responder"),
                "team": staff.get("team"),
                "status": "en_route",
                "eta_seconds": 180,
                "unit_label": staff.get("assignment_label", "Unit"),
            },
        )

        return AssignResponderResponse(success=True, assignment_id=assignment_id)

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
                "created_at": datetime.now(UTC),
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

    @staticmethod
    def _staff_locations(rows: list[dict], floor: int) -> list[StaffLocation]:
        output: list[StaffLocation] = []
        for idx, row in enumerate(rows):
            assignment = row.get("assignment", {})
            status = row.get("status", StaffDirectoryStatus.AVAILABLE)
            if status == StaffDirectoryStatus.OFF_DUTY:
                continue
            output.append(
                StaffLocation(
                    employee_id=row.get("employee_id", ""),
                    lat=float(row.get("lat", 19.0 + idx * 0.0001)),
                    lng=float(row.get("lng", 72.0 + idx * 0.0001)),
                    floor=int(assignment.get("floor", floor)),
                    status=status,
                )
            )
        return output

    @staticmethod
    def _guest_heatmap(rows: list[dict]) -> list[GuestHeatmapPoint]:
        by_zone: dict[str, dict] = {}
        for idx, row in enumerate(rows):
            zone = row.get("zone_id") or f"zone-{row.get('room_id', idx)}"
            if zone not in by_zone:
                by_zone[zone] = {
                    "zone_id": zone,
                    "lat": float(row.get("lat", 19.1 + idx * 0.0001)),
                    "lng": float(row.get("lng", 72.1 + idx * 0.0001)),
                    "count": 0,
                }
            by_zone[zone]["count"] += 1

        return [GuestHeatmapPoint(**z) for z in by_zone.values()]

    def _incident_points(self, incidents: list[dict]) -> list[ActiveIncidentMapPoint]:
        points: list[ActiveIncidentMapPoint] = []
        for incident in incidents:
            location = incident.get("location", {})
            coordinates = location.get("coordinates", {})
            incident_type = str(incident.get("type", "")).lower()
            if incident_type not in {"fire", "medical", "security"}:
                incident_type = "security"

            points.append(
                ActiveIncidentMapPoint(
                    incident_id=incident.get("incident_id", incident.get("id", "")),
                    lat=float(coordinates.get("lat", 0.0)),
                    lng=float(coordinates.get("lng", 0.0)),
                    type=IncidentPinType(incident_type),
                    severity=self._to_priority(incident.get("severity")),
                )
            )
        return points

    def _active_incident_card(self, incident: dict | None) -> ActiveIncidentCard | None:
        if not incident:
            return None

        location = incident.get("location", {})
        assignments = incident.get("responder_assignments", [])
        closest_staff = assignments[0] if assignments else {"name": "Unassigned", "role": "n/a"}

        return ActiveIncidentCard(
            incident_id=incident.get("incident_id", incident.get("id", "")),
            title=incident.get("title", "Incident"),
            incident_code=incident.get("incident_code", incident.get("event_code", "INC-UNKNOWN")),
            auto_triggered=bool(incident.get("auto_triggered", False)),
            elapsed_seconds=self._elapsed_seconds(incident),
            location=IncidentCardLocation(
                floor=int(location.get("floor", 0)),
                room=str(location.get("room", "N/A")),
                sector=str(location.get("sector", location.get("zone", "Unknown"))),
            ),
            sensor_status="active" if incident.get("sensor_status", True) else "inactive",
            proximity_guests=len(incident.get("guest_accountability", [])),
            closest_staff=ClosestStaff(name=closest_staff.get("name", "Unassigned"), role=closest_staff.get("role", "n/a")),
            dispatched_units=[
                DispatchedUnit(
                    employee_id=row.get("employee_id", ""),
                    name=row.get("name", "Responder"),
                    avatar_url=row.get("avatar_url"),
                    status=row.get("status", "en_route"),
                    eta_seconds=row.get("eta_seconds"),
                )
                for row in assignments
            ],
        )

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
        current = AdminMapService._to_priority(raw)
        if current == CrisisPriority.P3:
            return CrisisPriority.P2
        return CrisisPriority.P1

    @staticmethod
    def _elapsed_seconds(incident: dict) -> int:
        started_raw = incident.get("started_at") or incident.get("created_at")
        if isinstance(started_raw, datetime):
            started = started_raw if started_raw.tzinfo else started_raw.replace(tzinfo=UTC)
        elif isinstance(started_raw, str):
            parsed = datetime.fromisoformat(started_raw)
            started = parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)
        else:
            started = datetime.now(UTC)
        return max(int((datetime.now(UTC) - started).total_seconds()), 0)
