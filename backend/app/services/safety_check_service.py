"""
app/services/safety_check_service.py
Business logic for staff safety checks.
"""

from datetime import UTC, datetime, timedelta

from app.core.constants import ConnectivityStatus, DeviceHealth, ShiftStatus
from app.core.exceptions import NotFoundException
from app.db.repositories.safety_check_repository import SafetyCheckRepository
from app.db.repositories.staff_repository import StaffRepository
from app.schemas.staff.safety_check import (
    DeviceStatusInfo,
    SafetyCheckConfirmRequest,
    SafetyCheckConfirmResponse,
    SafetyCheckResponse,
    ShiftStatusInfo,
    Zone,
)

# How frequently a new safety check is generated (minutes)
SAFETY_CHECK_INTERVAL_MINUTES = 30


class SafetyCheckService:
    def __init__(
        self,
        safety_check_repo: SafetyCheckRepository,
        staff_repo: StaffRepository,
    ) -> None:
        self._repo = safety_check_repo
        self._staff_repo = staff_repo

    async def get_current_check(self, employee_id: str) -> SafetyCheckResponse:
        """
        Returns the most recent un-confirmed safety check for the employee.
        Creates a new one if none exists or the last one was already confirmed.
        """
        staff = await self._staff_repo.get_by_employee_id(employee_id)
        if not staff:
            raise NotFoundException(message="Staff member not found.")

        doc = await self._repo.get_latest_for_staff(employee_id)

        # Create a new check if there is none or the existing one is already confirmed
        if not doc or doc.get("confirmed_at") is not None:
            doc = await self._create_new_check(employee_id, staff)

        return self._to_response(doc)

    async def confirm_check(
        self, request: SafetyCheckConfirmRequest
    ) -> SafetyCheckConfirmResponse:
        doc = await self._repo.get_by_check_id(request.check_id)
        if not doc:
            raise NotFoundException(message="Safety check not found.")

        confirmed_at = datetime.fromisoformat(request.confirmed_at)
        await self._repo.confirm(
            request.check_id, confirmed_at, request.override_note
        )

        next_check_at = (
            datetime.now(UTC) + timedelta(minutes=SAFETY_CHECK_INTERVAL_MINUTES)
        ).isoformat()

        return SafetyCheckConfirmResponse(success=True, next_check_at=next_check_at)

    # ─── Helpers ─────────────────────────────────────────────────────────────

    async def _create_new_check(self, employee_id: str, staff: dict) -> dict:
        now = datetime.now(UTC)
        check_data = {
            "employee_id": employee_id,
            "generated_at": now,
            "confirmed_at": None,
            "zone_id": staff.get("current_zone_id", "ZONE-001"),
            "zone_label": staff.get("current_zone_label", "Main Entrance"),
            "zone_sector": staff.get("current_zone_sector", "A"),
            "zone_route": staff.get("current_zone_route", "/zones/zone-001"),
            "shift_status": staff.get("shift_status", ShiftStatus.ACTIVE),
            "shift_started_at": staff.get("checkin_time", now).isoformat()
            if not isinstance(staff.get("checkin_time"), str)
            else staff.get("checkin_time"),
            "device_health": DeviceHealth.OPTIMAL,
            "battery_percent": 85,
            "connectivity": ConnectivityStatus.ONLINE,
        }
        inserted_id = await self._repo.insert_one(check_data)
        check_data["id"] = inserted_id
        return check_data

    def _to_response(self, doc: dict) -> SafetyCheckResponse:
        now = datetime.now(UTC)
        shift_started = doc.get("shift_started_at", now.isoformat())
        if isinstance(shift_started, datetime):
            shift_started_dt = shift_started
        else:
            shift_started_dt = datetime.fromisoformat(str(shift_started))

        elapsed = int((now - shift_started_dt.replace(tzinfo=UTC)).total_seconds())

        generated_at = doc.get("generated_at", now)
        generated_at_str = (
            generated_at.isoformat()
            if isinstance(generated_at, datetime)
            else str(generated_at)
        )

        return SafetyCheckResponse(
            check_id=doc.get("id", ""),
            employee_id=doc["employee_id"],
            generated_at=generated_at_str,
            current_zone=Zone(
                zone_id=doc.get("zone_id", ""),
                label=doc.get("zone_label", ""),
                sector=doc.get("zone_sector", ""),
                route=doc.get("zone_route", ""),
            ),
            shift_status=ShiftStatusInfo(
                status=doc.get("shift_status", ShiftStatus.ACTIVE),
                started_at=str(shift_started),
                elapsed_seconds=max(elapsed, 0),
            ),
            device_status=DeviceStatusInfo(
                health=doc.get("device_health", DeviceHealth.OPTIMAL),
                battery_percent=doc.get("battery_percent", 100),
                connectivity=doc.get("connectivity", ConnectivityStatus.ONLINE),
            ),
        )
