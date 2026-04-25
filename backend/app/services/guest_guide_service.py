"""
app/services/guest_guide_service.py
Serves the guest-facing safety guidance screen for an active alert.
"""

from datetime import UTC, datetime

from app.core.constants import GuestAlertType, IncidentSeverity
from app.core.exceptions import NotFoundException
from app.db.repositories.alert_repository import AlertRepository
from app.db.repositories.guest_repository import GuestRepository, RoomRepository
from app.schemas.guest.guest import (
    EvacuationMap,
    GuestAlertGuideResponse,
    ImmediateAction,
    PrimaryInstruction,
    RoomContext,
    UserLocation,
)

# ── Playbook definitions (in production: load from DB / CMS) ────────────────
_PLAYBOOKS: dict[str, dict] = {
    "FIRE": {
        "alert_type": GuestAlertType.EVACUATE,
        "headline": "Fire Alert — Evacuate Immediately",
        "primary_instruction": PrimaryInstruction(
            title="Evacuate Now",
            body="Leave your room immediately using the nearest stairwell. Do NOT use elevators.",
            icon="flame",
        ),
        "immediate_actions": [
            ImmediateAction(
                step=1,
                title="Feel the door",
                body="Touch the door with the back of your hand. If hot, do not open.",
            ),
            ImmediateAction(
                step=2,
                title="Take essentials only",
                body="Grab your phone and key card. Leave everything else.",
            ),
            ImmediateAction(
                step=3,
                title="Use the stairwell",
                body="Walk briskly to the nearest emergency stairwell. Stay low if there is smoke.",
            ),
            ImmediateAction(
                step=4,
                title="Assemble outside",
                body="Proceed to the muster point at the society main gate.",
            ),
        ],
    },
    "MEDICAL": {
        "alert_type": GuestAlertType.SHELTER_IN_PLACE,
        "headline": "Medical Emergency — Help Is On The Way",
        "primary_instruction": PrimaryInstruction(
            title="Stay Calm & Shelter In Place",
            body="Medical responders are en route. Stay in your room unless instructed otherwise.",
            icon="heart-pulse",
        ),
        "immediate_actions": [
            ImmediateAction(
                step=1,
                title="Call for help",
                body="Dial 112 or use the emergency button in your room.",
            ),
            ImmediateAction(
                step=2,
                title="Unlock your door",
                body="Unlock your main door so responders can enter quickly.",
            ),
            ImmediateAction(
                step=3,
                title="Stay on the line",
                body="Keep your phone accessible and answer calls from responders.",
            ),
        ],
    },
    "SECURITY": {
        "alert_type": GuestAlertType.LOCKDOWN,
        "headline": "Security Alert — Lockdown In Effect",
        "primary_instruction": PrimaryInstruction(
            title="Lock Your Door & Stay Inside",
            body="A security situation is being managed. Lock your door and move away from windows.",
            icon="shield-alert",
        ),
        "immediate_actions": [
            ImmediateAction(
                step=1,
                title="Lock your door",
                body="Dead-bolt your door and do not open it for anyone.",
            ),
            ImmediateAction(
                step=2,
                title="Stay away from windows",
                body="Move to an interior wall or bathroom.",
            ),
            ImmediateAction(
                step=3,
                title="Silence your phone",
                body="Keep it on vibrate and await official announcements.",
            ),
        ],
    },
}

_DEFAULT_PLAYBOOK = {
    "alert_type": GuestAlertType.CUSTOM,
    "headline": "Emergency Alert — Please Follow Instructions",
    "primary_instruction": PrimaryInstruction(
        title="Await Instructions",
        body="An emergency has been reported. Stay calm and await instructions from society staff.",
        icon="alert-circle",
    ),
    "immediate_actions": [
        ImmediateAction(
            step=1, title="Stay calm", body="Do not panic. Help is on the way."
        ),
        ImmediateAction(
            step=2,
            title="Stay reachable",
            body="Keep your phone on and answer calls from management.",
        ),
    ],
}


class GuestGuideService:
    def __init__(
        self,
        alert_repo: AlertRepository,
        guest_repo: GuestRepository,
        room_repo: RoomRepository,
    ) -> None:
        self._alert_repo = alert_repo
        self._guest_repo = guest_repo
        self._room_repo = room_repo

    async def get_guide(self, alert_id: str, guest_id: str) -> GuestAlertGuideResponse:
        alert = await self._alert_repo.find_one({"alert_id": alert_id})
        if not alert:
            raise NotFoundException(message=f"Alert '{alert_id}' not found.")

        guest = await self._guest_repo.get_by_guest_id(guest_id)
        if not guest:
            raise NotFoundException(message="Guest not found.")

        room_id = guest.get("room_id", "")
        room = await self._room_repo.get_by_room_id(guest["property_id"], room_id)

        playbook = _PLAYBOOKS.get(alert.get("type_id", ""), _DEFAULT_PLAYBOOK)

        return GuestAlertGuideResponse(
            alert_id=alert_id,
            alert_type=playbook["alert_type"],
            severity=alert.get("severity", IncidentSeverity.WARNING),
            headline=playbook["headline"],
            room_context=RoomContext(
                room_id=room_id,
                room_number=room.get("room_number", room_id) if room else room_id,
                is_safe_zone=playbook["alert_type"] == GuestAlertType.SHELTER_IN_PLACE,
                safe_zone_note=(
                    "Your room is designated as a safe zone during this event."
                    if playbook["alert_type"] == GuestAlertType.SHELTER_IN_PLACE
                    else None
                ),
            ),
            primary_instruction=playbook["primary_instruction"],
            immediate_actions=playbook["immediate_actions"],
            evacuation_map=EvacuationMap(
                available=True,
                map_url=f"/maps/{guest['property_id']}/floor/{room.get('floor', 1) if room else 1}",
                user_location=UserLocation(label=f"Room {room_id}"),
            ),
            last_updated_at=datetime.now(UTC).isoformat(),
        )
