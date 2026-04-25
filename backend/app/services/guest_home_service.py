"""
app/services/guest_home_service.py
Business logic for the resident-facing home screen.
"""

from app.core.constants import IncidentSeverity, InfoHubCategory
from app.core.exceptions import NotFoundException
from app.db.repositories.guest_repository import GuestRepository, RoomRepository
from app.db.repositories.incident_repository import IncidentRepository
from app.schemas.guest.guest import (
    ActiveAlertBanner,
    GuestHomeResponse,
    GuestProfile,
    InfoHubItem,
    QuickAction,
)

# Static quick actions available to all residents
_QUICK_ACTIONS = [
    QuickAction(
        id="raise_alert",
        label="Raise Alert",
        description="Report an emergency or hazard",
        icon="alert-triangle",
        route="/alert/raise",
        enabled=True,
    ),
    QuickAction(
        id="evacuation_guide",
        label="Evacuation Guide",
        description="Step-by-step evacuation instructions",
        icon="map-pin",
        route="/guide/evacuation",
        enabled=True,
    ),
    QuickAction(
        id="contact_security",
        label="Contact Security",
        description="Direct line to on-duty security",
        icon="shield",
        route="/contact/security",
        enabled=True,
    ),
    QuickAction(
        id="emergency_contacts",
        label="Emergency Contacts",
        description="Police, Fire, Ambulance numbers",
        icon="phone",
        route="/contacts/emergency",
        enabled=True,
    ),
]

_INFO_HUB = [
    InfoHubItem(
        id="fire_protocol",
        category=InfoHubCategory.PROTOCOL,
        title="Fire Safety Protocol",
        preview="What to do if you smell smoke or see fire",
        route="/info/fire-protocol",
        thumbnail_url=None,
    ),
    InfoHubItem(
        id="medical_emergency",
        category=InfoHubCategory.PROTOCOL,
        title="Medical Emergency Guide",
        preview="First aid steps while help is on the way",
        route="/info/medical-guide",
        thumbnail_url=None,
    ),
    InfoHubItem(
        id="society_contacts",
        category=InfoHubCategory.RESOURCE,
        title="Society Contact Directory",
        preview="Management office, maintenance, security",
        route="/info/contacts",
        thumbnail_url=None,
    ),
]


class GuestHomeService:
    def __init__(
        self,
        guest_repo: GuestRepository,
        incident_repo: IncidentRepository,
    ) -> None:
        self._guest_repo = guest_repo
        self._incident_repo = incident_repo

    async def get_home(self, guest_id: str) -> GuestHomeResponse:
        guest = await self._guest_repo.get_by_guest_id(guest_id)
        if not guest:
            raise NotFoundException(message="Guest profile not found.")

        active_incident = await self._incident_repo.get_active_for_property(
            guest["property_id"]
        )
        alert_banner = self._build_alert_banner(active_incident)

        return GuestHomeResponse(
            guest=GuestProfile(
                name=guest.get("name", "Resident"),
                property_name=guest.get("property_name", "Housing Society"),
                room_id=guest.get("room_id", ""),
            ),
            active_alert=alert_banner,
            quick_actions=_QUICK_ACTIONS,
            info_hub=_INFO_HUB,
            sos_enabled=True,
        )

    def _build_alert_banner(self, incident: dict | None) -> ActiveAlertBanner:
        if not incident:
            return ActiveAlertBanner(present=False)
        return ActiveAlertBanner(
            present=True,
            alert_id=incident.get("id"),
            severity=incident.get("severity", IncidentSeverity.WARNING),
            title=incident.get("title"),
            body=incident.get("description"),
            cta_label="View Safety Guide",
            cta_route=f"/guest/alert/{incident.get('id')}/guide",
        )