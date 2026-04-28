"""
app/services/guest_alert_guide_service.py
"""

from datetime import UTC, datetime

from app.core.constants import AlertGuideType, GuestErrorCode, IncidentSeverity
from app.core.exceptions import NotFoundException
from app.db.repositories.alert_repository import AlertRepository
from app.db.repositories.guest_repository import GuestRepository, RoomRepository
from app.db.repositories.incident_command_repository import IncidentCommandRepository
from app.schemas.guest.alert import (
    EvacuationMap,
    GuestAlertGuideResponse,
    ImmediateAction,
    PrimaryInstruction,
    RoomContext,
    UserLocation,
)


class GuestAlertGuideService:
    def __init__(
        self,
        alert_repo: AlertRepository,
        incident_repo: IncidentCommandRepository,
        guest_repo: GuestRepository,
        room_repo: RoomRepository,
    ) -> None:
        self._alert_repo = alert_repo
        self._incident_repo = incident_repo
        self._guest_repo = guest_repo
        self._room_repo = room_repo

    async def get_guide(
        self,
        alert_id: str,
        guest_id: str | None = None,
    ) -> GuestAlertGuideResponse:
        alert = await self._alert_repo.get_by_alert_id(alert_id)
        incident_id = alert.get("incident_id") if alert else alert_id
        incident = await self._incident_repo.get_by_incident_id(str(incident_id))

        if not alert and not incident:
            raise NotFoundException(
                code=GuestErrorCode.ALERT_GUIDE_NOT_FOUND,
                message=f"Alert guide for '{alert_id}' was not found.",
            )

        alert_type = self._resolve_alert_type(alert, incident)
        severity = self._resolve_severity(alert, incident)
        guest = await self._resolve_guest(guest_id)
        room = await self._room_repo.get_by_room_id(guest.get("room_id", ""))

        room_context = RoomContext(
            room_id=guest.get("room_id", "UNKNOWN"),
            room_number=(room or {}).get("room_number", guest.get("room_number", "Unknown")),
            is_safe_zone=bool((room or {}).get("is_safe_zone", False)),
            safe_zone_note=(room or {}).get("safe_zone_note"),
        )

        incident_title = (incident or {}).get("title") or (alert or {}).get("type_id", "Alert")
        location = (alert or {}).get("location", {})

        return GuestAlertGuideResponse(
            alert_id=alert_id,
            alert_type=alert_type,
            severity=severity,
            headline=f"{incident_title} - Follow these steps immediately",
            room_context=room_context,
            primary_instruction=self._primary_instruction(alert_type),
            immediate_actions=self._immediate_actions(alert_type),
            evacuation_map=EvacuationMap(
                available=True,
                map_url=(incident or {}).get("evacuation_map_url"),
                user_location=UserLocation(
                    lat=location.get("lat"),
                    lng=location.get("lng"),
                    label=location.get("manual_label"),
                ),
            ),
            last_updated_at=self._to_iso((incident or {}).get("updated_at")),
        )

    async def _resolve_guest(self, guest_id: str | None) -> dict:
        guest = None
        if guest_id:
            guest = await self._guest_repo.get_by_guest_id(guest_id)
        if not guest:
            guest = await self._guest_repo.get_default()
        if not guest:
            raise NotFoundException(
                code=GuestErrorCode.GUEST_NOT_FOUND,
                message="Guest profile not found.",
            )
        return guest

    @staticmethod
    def _resolve_alert_type(alert: dict | None, incident: dict | None) -> AlertGuideType:
        incident_type = str((incident or {}).get("type", "")).lower()
        if incident_type == "fire":
            return AlertGuideType.EVACUATE
        if incident_type == "security":
            return AlertGuideType.LOCKDOWN
        if incident_type == "medical":
            return AlertGuideType.MEDICAL

        type_id = str((alert or {}).get("type_id", "")).lower()
        if type_id == "fire":
            return AlertGuideType.EVACUATE
        if type_id == "security":
            return AlertGuideType.LOCKDOWN
        if type_id == "medical":
            return AlertGuideType.MEDICAL
        return AlertGuideType.CUSTOM

    @staticmethod
    def _resolve_severity(alert: dict | None, incident: dict | None) -> IncidentSeverity:
        raw = str((incident or {}).get("severity") or (alert or {}).get("severity") or "info")
        if raw in (IncidentSeverity.INFO, IncidentSeverity.WARNING, IncidentSeverity.CRITICAL):
            return IncidentSeverity(raw)
        if raw == "P1":
            return IncidentSeverity.CRITICAL
        if raw == "P2":
            return IncidentSeverity.WARNING
        return IncidentSeverity.INFO

    @staticmethod
    def _primary_instruction(alert_type: AlertGuideType) -> PrimaryInstruction:
        if alert_type == AlertGuideType.EVACUATE:
            return PrimaryInstruction(
                title="Evacuate using nearest safe exit",
                body="Leave belongings behind and use staircases, not elevators.",
                icon="door-open",
            )
        if alert_type == AlertGuideType.LOCKDOWN:
            return PrimaryInstruction(
                title="Secure your location",
                body="Lock doors, stay away from windows, and remain silent.",
                icon="shield-lock",
            )
        if alert_type == AlertGuideType.MEDICAL:
            return PrimaryInstruction(
                title="Prepare for medical response",
                body="Keep pathways clear for responders and monitor patient status.",
                icon="heart-pulse",
            )

        return PrimaryInstruction(
            title="Follow on-screen instructions",
            body="Stay calm and follow staff guidance shared through this app.",
            icon="info",
        )

    @staticmethod
    def _immediate_actions(alert_type: AlertGuideType) -> list[ImmediateAction]:
        if alert_type == AlertGuideType.EVACUATE:
            return [
                ImmediateAction(step=1, title="Check corridor", body="Ensure corridor is safe before opening the door."),
                ImmediateAction(step=2, title="Use staircase", body="Proceed to the nearest marked evacuation staircase."),
                ImmediateAction(step=3, title="Reach assembly point", body="Move to the assembly point and wait for updates."),
            ]

        if alert_type == AlertGuideType.LOCKDOWN:
            return [
                ImmediateAction(step=1, title="Lock all access points", body="Lock room doors and close curtains/blinds."),
                ImmediateAction(step=2, title="Silence devices", body="Keep all devices on silent to avoid drawing attention."),
                ImmediateAction(step=3, title="Await official update", body="Only move once security gives an all-clear."),
            ]

        return [
            ImmediateAction(step=1, title="Stay calm", body="Take a deep breath and avoid crowding exits."),
            ImmediateAction(step=2, title="Follow directions", body="Follow app prompts and on-ground responder instructions."),
            ImmediateAction(step=3, title="Confirm safety", body="Use check-in when prompted so responders can track your status."),
        ]

    @staticmethod
    def _to_iso(value: object | None) -> str:
        if value is None:
            return datetime.now(UTC).isoformat()
        if isinstance(value, datetime):
            return value.isoformat()
        return str(value)
