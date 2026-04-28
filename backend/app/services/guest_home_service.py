"""
app/services/guest_home_service.py
"""

from app.core.constants import IncidentSeverity, InfoHubCategory
from app.core.exceptions import NotFoundException
from app.db.repositories.admin_repository import PropertyRepository
from app.db.repositories.guest_repository import GuestRepository
from app.db.repositories.incident_command_repository import IncidentCommandRepository
from app.schemas.guest.home import (
    GuestActiveAlert,
    GuestHomeResponse,
    GuestSummary,
    InfoHubItem,
    QuickActionItem,
)


class GuestHomeService:
    def __init__(
        self,
        guest_repo: GuestRepository,
        property_repo: PropertyRepository,
        incident_repo: IncidentCommandRepository,
    ) -> None:
        self._guest_repo = guest_repo
        self._property_repo = property_repo
        self._incident_repo = incident_repo

    async def get_home(self, guest_id: str | None = None) -> GuestHomeResponse:
        guest = await self._resolve_guest(guest_id)

        property_doc = await self._property_repo.get_by_property_id(guest.get("property_id", ""))
        property_name = property_doc.get("name", "Property") if property_doc else "Property"

        incidents = await self._incident_repo.list_for_property(
            guest.get("property_id", ""),
            limit=1,
            include_resolved=False,
        )
        active_incident = incidents[0] if incidents else None

        return GuestHomeResponse(
            guest=GuestSummary(
                name=guest.get("name", "Guest"),
                property_name=property_name,
                room_id=guest.get("room_id", "UNKNOWN"),
            ),
            active_alert=self._to_active_alert(active_incident),
            quick_actions=self._quick_actions(),
            info_hub=self._info_hub(),
            sos_enabled=True,
        )

    async def _resolve_guest(self, guest_id: str | None) -> dict:
        guest = None
        if guest_id:
            guest = await self._guest_repo.get_by_guest_id(guest_id)
        if not guest:
            guest = await self._guest_repo.get_default()
        if not guest:
            raise NotFoundException(message="Guest profile not found.")
        return guest

    def _to_active_alert(self, incident: dict | None) -> GuestActiveAlert:
        if not incident:
            return GuestActiveAlert(present=False)

        incident_id = incident.get("incident_id") or incident.get("id")
        severity = self._normalize_severity(incident.get("severity"))
        return GuestActiveAlert(
            present=True,
            alert_id=str(incident_id),
            severity=severity,
            title=incident.get("title"),
            body=incident.get("description"),
            cta_label="View Guidance",
            cta_route=f"/guest/alert/{incident_id}/guide",
        )

    @staticmethod
    def _normalize_severity(raw: str | None) -> IncidentSeverity:
        if raw in (IncidentSeverity.INFO, IncidentSeverity.WARNING, IncidentSeverity.CRITICAL):
            return IncidentSeverity(raw)

        if raw == "P1":
            return IncidentSeverity.CRITICAL
        if raw == "P2":
            return IncidentSeverity.WARNING
        return IncidentSeverity.INFO

    @staticmethod
    def _quick_actions() -> list[QuickActionItem]:
        return [
            QuickActionItem(
                id="raise_alert",
                label="Raise Alert",
                description="Report fire, medical, or security emergency instantly.",
                icon="siren",
                route="/guest/alert/raise",
                enabled=True,
            ),
            QuickActionItem(
                id="view_guidance",
                label="Safety Guidance",
                description="View evacuation and shelter instructions.",
                icon="shield-check",
                route="/guest/guidance",
                enabled=True,
            ),
            QuickActionItem(
                id="support",
                label="Contact Front Desk",
                description="Reach on-site support for assistance.",
                icon="phone",
                route="/guest/support",
                enabled=True,
            ),
        ]

    @staticmethod
    def _info_hub() -> list[InfoHubItem]:
        return [
            InfoHubItem(
                id="fire_protocol",
                category=InfoHubCategory.PROTOCOL,
                title="Fire Evacuation Protocol",
                preview="Know the nearest exits and staircase routes.",
                route="/guest/info/fire-protocol",
            ),
            InfoHubItem(
                id="medical_resource",
                category=InfoHubCategory.RESOURCE,
                title="Medical Help Desk",
                preview="Find emergency contacts and first-aid points.",
                route="/guest/info/medical-resource",
            ),
            InfoHubItem(
                id="safety_notice",
                category=InfoHubCategory.NOTICE,
                title="Current Safety Notice",
                preview="Stay informed about maintenance and risk advisories.",
                route="/guest/info/notices",
            ),
        ]
