"""
app/services/admin_overview_service.py
"""

from datetime import UTC, datetime

from app.core.constants import (
    CrisisPriority,
    IncidentPinType,
    IncidentQueueStatus,
    ResponderUnitStatus,
    StaffDirectoryStatus,
)
from app.db.repositories.admin_repository import PropertyRepository, StaffDirectoryRepository
from app.db.repositories.guest_repository import GuestRepository, RoomRepository
from app.db.repositories.incident_command_repository import IncidentCommandRepository
from app.schemas.admin.overview import (
    ActiveIncidentBanner,
    ActiveResponderCard,
    AdminOverviewResponse,
    IncidentPin,
    IncidentQueueItem,
    LiveMapSummary,
    OverviewKPIs,
    PropertySummary,
)


class AdminOverviewService:
    def __init__(
        self,
        property_repo: PropertyRepository,
        incident_repo: IncidentCommandRepository,
        staff_repo: StaffDirectoryRepository,
        guest_repo: GuestRepository,
        room_repo: RoomRepository,
    ) -> None:
        self._property_repo = property_repo
        self._incident_repo = incident_repo
        self._staff_repo = staff_repo
        self._guest_repo = guest_repo
        self._room_repo = room_repo

    async def get_overview(self, property_id: str | None = None) -> AdminOverviewResponse:
        property_doc = await self._resolve_property(property_id)
        pid = property_doc["property_id"]

        incidents = await self._incident_repo.list_for_property(pid, limit=20, include_resolved=True)
        active_incidents = [i for i in incidents if i.get("status") != "resolved"]
        lead_incident = active_incidents[0] if active_incidents else None

        staff_on_duty = await self._staff_repo.count_on_shift(pid)
        guests_tracked = await self._guest_repo.count_tracked(pid)
        avg_response = self._avg_response_time(incidents)
        floors = await self._room_repo.list_floors(pid)

        return AdminOverviewResponse(
            property=PropertySummary(
                property_id=pid,
                name=property_doc.get("name", "Property"),
                server_time=datetime.now(UTC).isoformat(),
            ),
            active_incident_banner=self._banner(lead_incident),
            kpis=OverviewKPIs(
                staff_on_duty=staff_on_duty,
                active_incidents=len(active_incidents),
                guests_tracked=guests_tracked,
                avg_response_time_seconds=avg_response,
            ),
            live_map_summary=self._map_summary(lead_incident, floors),
            active_responders=await self._active_responders(pid),
            incident_queue=self._incident_queue(incidents),
        )

    async def _resolve_property(self, property_id: str | None) -> dict:
        property_doc = None
        if property_id:
            property_doc = await self._property_repo.get_by_property_id(property_id)
        if not property_doc:
            property_doc = await self._property_repo.get_default()
        if not property_doc:
            property_doc = {
                "property_id": "PROP-DEFAULT",
                "name": "Rapid Response Property",
            }
        return property_doc

    def _banner(self, incident: dict | None) -> ActiveIncidentBanner:
        if not incident:
            return ActiveIncidentBanner(present=False)

        incident_id = incident.get("incident_id") or incident.get("id")
        severity = self._to_priority(incident.get("severity"))
        responders_deployed = len(incident.get("responder_assignments", []))
        guests_in_zone = len(incident.get("guest_accountability", []))

        return ActiveIncidentBanner(
            present=True,
            incident_id=str(incident_id),
            title=incident.get("title"),
            severity=severity,
            responders_deployed=responders_deployed,
            guests_in_zone=guests_in_zone,
            cta_route=f"/admin/incident/{incident_id}",
        )

    def _map_summary(self, incident: dict | None, floors: list[int]) -> LiveMapSummary:
        location = (incident or {}).get("location", {})
        coordinates = location.get("coordinates", {})

        incident_type = str((incident or {}).get("type", "")).lower()
        if incident_type not in {"fire", "medical", "security"}:
            map_type = None
        else:
            map_type = IncidentPinType(incident_type)

        floor = location.get("floor")
        active_floor = int(floor) if floor is not None else (floors[0] if floors else 0)

        return LiveMapSummary(
            active_floor=active_floor,
            floors=floors or [active_floor],
            incident_pin=IncidentPin(
                lat=coordinates.get("lat"),
                lng=coordinates.get("lng"),
                floor=int(floor) if floor is not None else None,
                type=map_type,
            ),
        )

    async def _active_responders(self, property_id: str) -> list[ActiveResponderCard]:
        rows = await self._staff_repo.list_active_responders(property_id, limit=12)
        cards: list[ActiveResponderCard] = []
        for row in rows:
            name = row.get("name", "Staff")
            parts = [p for p in name.split(" ") if p]
            initials = "".join(p[0] for p in parts[:2]).upper() or "NA"
            cards.append(
                ActiveResponderCard(
                    employee_id=row.get("employee_id", ""),
                    name=name,
                    initials=initials,
                    role=row.get("role", "staff"),
                    status=self._map_responder_status(row.get("status")),
                )
            )
        return cards

    def _incident_queue(self, incidents: list[dict]) -> list[IncidentQueueItem]:
        now = datetime.now(UTC)
        items: list[IncidentQueueItem] = []
        for row in incidents[:20]:
            created = self._to_datetime(row.get("created_at"))
            age_seconds = max(int((now - created).total_seconds()), 0)
            location = row.get("location", {})
            zone = location.get("zone") or location.get("area_name") or "Unknown"
            floor = location.get("floor")
            label = f"Floor {floor} - {zone}" if floor is not None else zone
            items.append(
                IncidentQueueItem(
                    incident_id=row.get("incident_id", row.get("id", "")),
                    title=row.get("title", "Incident"),
                    location=label,
                    status=self._queue_status(row.get("status")),
                    age_seconds=age_seconds,
                )
            )
        return items

    @staticmethod
    def _avg_response_time(incidents: list[dict]) -> int:
        values: list[int] = []
        for incident in incidents:
            value = (incident.get("kpis") or {}).get("response_time_seconds")
            if isinstance(value, int):
                values.append(value)
        if not values:
            return 0
        return int(sum(values) / len(values))

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
    def _map_responder_status(raw: str | None) -> ResponderUnitStatus:
        if raw == StaffDirectoryStatus.RESPONDING:
            return ResponderUnitStatus.ON_SCENE
        if raw == StaffDirectoryStatus.AVAILABLE:
            return ResponderUnitStatus.STANDBY
        return ResponderUnitStatus.EN_ROUTE

    @staticmethod
    def _queue_status(raw: str | None) -> IncidentQueueStatus:
        if raw in (
            IncidentQueueStatus.ACTIVE,
            IncidentQueueStatus.INVESTIGATING,
            IncidentQueueStatus.RESOLVED,
        ):
            return IncidentQueueStatus(raw)
        if raw == "contained":
            return IncidentQueueStatus.INVESTIGATING
        return IncidentQueueStatus.ACTIVE

    @staticmethod
    def _to_datetime(value: object | None) -> datetime:
        if isinstance(value, datetime):
            return value if value.tzinfo else value.replace(tzinfo=UTC)
        if isinstance(value, str):
            parsed = datetime.fromisoformat(value)
            return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)
        return datetime.now(UTC)
