"""
app/services/auth_service.py
Business logic for staff authentication.
"""

from datetime import UTC, datetime, timedelta

from app.core.config import get_settings
from app.core.constants import AuthErrorCode
from app.core.exceptions import AccountLockedException, UnauthorizedException
from app.core.security import create_access_token, create_refresh_token, verify_password
from app.db.repositories.staff_repository import StaffRepository
from app.schemas.staff.auth import (
    PropertyNetworkInfo,
    StaffLoginRequest,
    StaffLoginResponse,
    StaffProfile,
)

settings = get_settings()


class AuthService:
    def __init__(self, staff_repo: StaffRepository) -> None:
        self._staff_repo = staff_repo

    async def login(self, request: StaffLoginRequest) -> StaffLoginResponse:
        staff = await self._staff_repo.get_by_employee_id(request.employee_id)

        if not staff:
            raise UnauthorizedException(
                code=AuthErrorCode.INVALID_CREDENTIALS,
                message="Invalid employee ID or PIN.",
            )

        # ── Lock check ───────────────────────────────────────────────────────
        locked_until = staff.get("locked_until")
        if locked_until and datetime.now(UTC) < locked_until:
            raise AccountLockedException(
                f"Account locked. Try again after {locked_until.isoformat()}."
            )

        # ── PIN verification ─────────────────────────────────────────────────
        print(staff)
        if not verify_password(request.pin, staff.get("pin_hash", "")):
            attempts = await self._staff_repo.increment_failed_attempts(request.employee_id)
            if attempts >= settings.max_login_attempts:
                lock_until = datetime.now(UTC) + timedelta(
                    minutes=settings.account_lock_duration_minutes
                )
                await self._staff_repo.lock_account(request.employee_id, lock_until)
                raise AccountLockedException()
            raise UnauthorizedException(
                code=AuthErrorCode.INVALID_CREDENTIALS,
                message="Invalid employee ID or PIN.",
            )

        # ── Property / network validation ────────────────────────────────────
        property_network = await self._validate_property_network(
            request.property_network_id, staff.get("property_id", "")
        )

        # ── Reset failed attempts on success ─────────────────────────────────
        await self._staff_repo.reset_failed_attempts(request.employee_id)
        await self._staff_repo.update_last_login(request.employee_id, request.device_id)

        # ── Issue tokens ─────────────────────────────────────────────────────
        access_token, expires_in = create_access_token(
            request.employee_id, extra={"role": staff["role"], "property_id": staff["property_id"]}
        )
        refresh_token = create_refresh_token(request.employee_id)

        return StaffLoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=expires_in,
            staff=StaffProfile(
                employee_id=staff["employee_id"],
                name=staff["name"],
                role=staff["role"],
                avatar_url=staff.get("avatar_url"),
                property_id=staff["property_id"],
            ),
            property_network=property_network,
            biometrics_enabled=settings.feature_biometrics_enabled,
        )

    async def _validate_property_network(
        self, network_id: str, staff_property_id: str
    ) -> PropertyNetworkInfo:
        """
        In production this would query the property network registry.
        For now we validate that the network_id matches the staff's property.
        """
        detected = network_id == staff_property_id
        return PropertyNetworkInfo(
            detected=detected,
            property_name="Housing Society" if detected else None,
            network_label=network_id if detected else None,
            secure_protocol=detected,
        )
