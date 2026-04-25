"""
app/services/admin_overview_service.py
Business logic for the admin overview dashboard.
"""

from datetime import UTC, datetime

from app.core.constants import DutyStatus, IncidentPriority, IncidentStatus
from app.core.exceptions import NotFoundException
from app.db.repositories.incident_repository import IncidentRepository
from app.db.repositories.staff_repository import StaffRepository
from app.db.repositories.guest_repository import GuestRepository
from app.schemas.admin.overview import (
    ActiveIncidentBanner,
    ActiveResponderCard,
    AdminKPIs,
    AdminOverviewResponse,
    IncidentPin,
    IncidentQueueItem,
    LiveMapSummary,
    PropertyInfo,
)


class AdminOverviewService:
    def __init__(
        self,
        incident_repo: IncidentRepository,
        staff_repo: StaffRepository,
        guest_repo: GuestRepository,
    ) -> None:
        self._incident_repo = incident_repo
        self._staff_repo = staff_repo
        self._guest_repo = guest_repo

    async def get_overview(self, property_id: str) -> AdminOverviewResponse:
        now = datetime.now(UTC)

        # ── Active incident ───────────────────────────────────────────────────
        active_incident = await self._incident_repo.get_active_for_property(property_id)
        banner = self._build_banner(active_incident)

        # ── KPIs ─────────────────────────────────────────────────────────────
        staff_on_duty = await self._staff_repo.count(
            {"property_id": property_id, "duty_status": DutyStatus.ON_DUTY}
        )
        guests_tracked = await self._guest_repo.count_tracked(property_id)
        active_incidents = await self._incident_repo.count(
            {"property_id": property_id, "status": IncidentStatus.ACTIVE}
        )

        # ── Recent incident queue ─────────────────────────────────────────────
        recent = await self._incident_repo.list_for_property(property_id, limit=10)
        queue = [
            IncidentQueueItem(
                incident_id=inc.get("id", ""),
                title=inc.get("title", ""),
                location=inc.get("area_name", "Unknown"),
                status=inc.get("status", IncidentStatus.ACTIVE),
                age_seconds=(
                    int((now - inc["created_at"].replace(tzinfo=UTC)).total_seconds())
                    if isinstance(inc.get("created_at"), datetime)
                    else 0
                ),
            )
            for inc in recent
        ]

        # ── Active responders ─────────────────────────────────────────────────
        on_duty_staff = await self._staff_repo.find_many(
            {"property_id": property_id, "duty_status": DutyStatus.ON_DUTY},
            limit=8,
        )
        responders = [
            ActiveResponderCard(
                employee_id=s["employee_id"],
                name=s["name"],
                initials="".join(p[0].upper() for p in s["name"].split()[:2]),
                role=s["role"],
                status=s.get("operational_status", "available"),
            )
            for s in on_duty_staff
        ]

        return AdminOverviewResponse(
            property=PropertyInfo(
                property_id=property_id,
                name="Housing Society",  # TODO: fetch from properties collection
                server_time=now.isoformat(),
            ),
            active_incident_banner=banner,
            kpis=AdminKPIs(
                staff_on_duty=staff_on_duty,
                active_incidents=active_incidents,
                guests_tracked=guests_tracked,
                avg_response_time_seconds=120,  # TODO: compute from incident KPIs
            ),
            live_map_summary=LiveMapSummary(
                active_floor=1,
                floors=[0, 1, 2, 3, 4, 5],
                incident_pin=IncidentPin(
                    lat=active_incident.get("lat") if active_incident else None,
                    lng=active_incident.get("lng") if active_incident else None,
                    floor=active_incident.get("floor") if active_incident else None,
                    type=active_incident.get("type") if active_incident else None,
                ),
            ),
            active_responders=responders,
            incident_queue=queue,
        )

    def _build_banner(self, incident: dict | None) -> ActiveIncidentBanner:
        if not incident:
            return ActiveIncidentBanner(present=False)
        return ActiveIncidentBanner(
            present=True,
            incident_id=incident.get("id"),
            title=incident.get("title"),
            severity=IncidentPriority.P1,
            responders_deployed=len(incident.get("responder_assignments", [])),
            guests_in_zone=incident.get("proximity_guests", 0),
            cta_route=f"/admin/incident/{incident.get('id')}",
        )
