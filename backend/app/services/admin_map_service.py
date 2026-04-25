"""
app/services/admin_map_service.py
Business logic for the admin live map and responder assignment.
"""

import uuid

from app.core.constants import IncidentPriority
from app.core.exceptions import NotFoundException
from app.db.repositories.incident_repository import IncidentRepository
from app.db.repositories.staff_repository import StaffRepository
from app.db.repositories.guest_repository import GuestRepository
from app.schemas.admin.map import (
    ActiveIncidentCard,
    AssignResponderRequest,
    AssignResponderResponse,
    BroadcastRequest,
    BroadcastResponse,
    CCTVCamera,
    ClosestStaff,
    DispatchedUnit,
    EscalateRequest,
    EscalateResponse,
    GuestHeatmapZone,
    IncidentMapPin,
    MapDataResponse,
    MapLayers,
    MapSummary,
    StaffLocationPin,
)
from app.db.repositories.admin_repository import BroadcastRepository


class AdminMapService:
    def __init__(
        self,
        incident_repo: IncidentRepository,
        staff_repo: StaffRepository,
        guest_repo: GuestRepository,
        broadcast_repo: BroadcastRepository,
    ) -> None:
        self._incident_repo = incident_repo
        self._staff_repo = staff_repo
        self._guest_repo = guest_repo
        self._broadcast_repo = broadcast_repo

    async def get_map_data(self, property_id: str, floor: int) -> MapDataResponse:
        # ── Staff locations ───────────────────────────────────────────────────
        staff_on_duty = await self._staff_repo.find_many(
            {"property_id": property_id, "duty_status": {"$ne": "off_duty"}}
        )
        staff_pins = [
            StaffLocationPin(
                employee_id=s["employee_id"],
                lat=s.get("lat", 0.0),
                lng=s.get("lng", 0.0),
                floor=s.get("current_floor", floor),
                status=s.get("operational_status", "available"),
            )
            for s in staff_on_duty
            if s.get("current_floor", floor) == floor
        ]

        # ── Active incidents ──────────────────────────────────────────────────
        active_incidents = await self._incident_repo.find_many(
            {"property_id": property_id, "status": "active"},
            limit=20,
        )
        incident_pins = [
            IncidentMapPin(
                incident_id=inc.get("id", ""),
                lat=inc.get("lat", 0.0),
                lng=inc.get("lng", 0.0),
                type=inc.get("type", "custom"),
                severity=IncidentPriority.P1,
            )
            for inc in active_incidents
        ]

        # ── Guest heatmap (aggregated, privacy-safe) ──────────────────────────
        heatmap: list[GuestHeatmapZone] = []  # TODO: aggregate from zone tracker

        # ── Active incident card ──────────────────────────────────────────────
        current_incident = active_incidents[0] if active_incidents else None
        card = (
            self._build_incident_card(current_incident, staff_on_duty)
            if current_incident
            else None
        )

        guests_present = await self._guest_repo.count_tracked(property_id)

        return MapDataResponse(
            property_id=property_id,
            floor=floor,
            floors_available=[0, 1, 2, 3, 4, 5],
            summary=MapSummary(
                staff_online=len(staff_on_duty),
                guests_present=guests_present,
                active_incidents=len(active_incidents),
                live_feed_syncing=True,
            ),
            layers=MapLayers(
                staff_locations=staff_pins,
                guest_heatmap=heatmap,
                active_incidents=incident_pins,
                cctv_cameras=[],  # TODO: load from cctv_cameras collection
            ),
            active_incident_card=card,
        )

    async def assign_responder(
        self, incident_id: str, request: AssignResponderRequest
    ) -> AssignResponderResponse:
        incident = await self._incident_repo.get_by_id(incident_id)
        if not incident:
            raise NotFoundException(message="Incident not found.")

        assignment_id = str(uuid.uuid4())
        await self._incident_repo.update_one(
            {"incident_id": incident_id},
            {
                "$push": {
                    "responder_assignments": {
                        "assignment_id": assignment_id,
                        "employee_id": request.employee_id,
                        "assigned_by": request.assigned_by,
                        "status": "dispatched",
                    }
                }
            },
        )
        return AssignResponderResponse(success=True, assignment_id=assignment_id)

    async def escalate_incident(
        self, incident_id: str, request: EscalateRequest
    ) -> EscalateResponse:
        incident = await self._incident_repo.get_by_id(incident_id)
        if not incident:
            raise NotFoundException(message="Incident not found.")

        current = incident.get("severity", IncidentPriority.P3)
        new_severity = (
            IncidentPriority.P1
            if current != IncidentPriority.P1
            else IncidentPriority.P1
        )

        await self._incident_repo.update_one(
            {"incident_id": incident_id},
            {"$set": {"severity": new_severity}},
        )
        return EscalateResponse(success=True, new_severity=new_severity)

    async def broadcast(self, request: BroadcastRequest) -> BroadcastResponse:
        broadcast_id = str(uuid.uuid4())
        await self._broadcast_repo.insert_one(
            {
                "broadcast_id": broadcast_id,
                "incident_id": request.incident_id,
                "audience": request.audience,
                "room_id": request.room_id,
                "message": request.message,
                "channels": request.channels,
                "sent_by": request.sent_by,
            }
        )
        # TODO: fan out to push/WhatsApp/SMS channels
        return BroadcastResponse(success=True, broadcast_id=broadcast_id, recipients=50)

    def _build_incident_card(
        self, incident: dict, staff: list[dict]
    ) -> ActiveIncidentCard:
        from datetime import UTC, datetime

        started_at = incident.get("created_at", datetime.now(UTC))
        elapsed = (
            int((datetime.now(UTC) - started_at.replace(tzinfo=UTC)).total_seconds())
            if isinstance(started_at, datetime)
            else 0
        )

        closest = staff[0] if staff else None

        return ActiveIncidentCard(
            incident_id=incident.get("id", ""),
            title=incident.get("title", ""),
            incident_code=incident.get("event_code", ""),
            auto_triggered=incident.get("auto_triggered", False),
            elapsed_seconds=elapsed,
            location={
                "floor": incident.get("floor", 0),
                "room": incident.get("room", ""),
                "sector": incident.get("sector", ""),
            },
            sensor_status=incident.get("sensor_status", "inactive"),
            proximity_guests=incident.get("proximity_guests", 0),
            closest_staff=ClosestStaff(
                name=closest["name"] if closest else "N/A",
                role=closest["role"] if closest else "",
            ),
            dispatched_units=[
                DispatchedUnit(
                    employee_id=r.get("employee_id", ""),
                    name=r.get("name", ""),
                    avatar_url=r.get("avatar_url"),
                    status=r.get("status", "dispatched"),
                    eta_seconds=r.get("eta_seconds"),
                )
                for r in incident.get("responder_assignments", [])
            ],
        )
