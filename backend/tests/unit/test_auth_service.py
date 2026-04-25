"""
tests/unit/test_auth_service.py
Unit tests for AuthService — no real DB, mocked repository.
"""

from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.core.constants import AuthErrorCode
from app.core.exceptions import AccountLockedException, UnauthorizedException
from app.schemas.staff.auth import StaffLoginRequest
from app.services.auth_service import AuthService


def _make_staff(**overrides) -> dict:
    base = {
        "employee_id": "EMP001",
        "name": "Test Staff",
        "pin_hash": "$2b$12$placeholder",  # will be patched
        "role": "security",
        "property_id": "PROP-HSG-001",
        "failed_attempts": 0,
        "locked_until": None,
        "avatar_url": None,
    }
    base.update(overrides)
    return base


def _make_request(**overrides) -> StaffLoginRequest:
    base = {
        "employee_id": "EMP001",
        "pin": "1234",
        "biometric_token": None,
        "device_id": "DEV-XYZ",
        "property_network_id": "PROP-HSG-001",
    }
    base.update(overrides)
    return StaffLoginRequest(**base)


@pytest.fixture
def staff_repo():
    repo = MagicMock()
    repo.get_by_employee_id = AsyncMock()
    repo.increment_failed_attempts = AsyncMock(return_value=1)
    repo.reset_failed_attempts = AsyncMock()
    repo.lock_account = AsyncMock()
    repo.update_last_login = AsyncMock()
    return repo


@pytest.fixture
def service(staff_repo):
    return AuthService(staff_repo)


# ── Tests ─────────────────────────────────────────────────────────────────────

class TestStaffLogin:
    async def test_login_success(self, service, staff_repo):
        staff_repo.get_by_employee_id.return_value = _make_staff()

        with patch("app.services.auth_service.verify_password", return_value=True):
            result = await service.login(_make_request())

        assert result.success is True
        assert result.staff.employee_id == "EMP001"
        assert result.access_token != ""
        assert result.expires_in > 0

    async def test_login_unknown_employee(self, service, staff_repo):
        staff_repo.get_by_employee_id.return_value = None

        with pytest.raises(UnauthorizedException) as exc_info:
            await service.login(_make_request())

        assert exc_info.value.code == AuthErrorCode.INVALID_CREDENTIALS

    async def test_login_wrong_pin(self, service, staff_repo):
        staff_repo.get_by_employee_id.return_value = _make_staff()

        with patch("app.services.auth_service.verify_password", return_value=False):
            with pytest.raises(UnauthorizedException) as exc_info:
                await service.login(_make_request(pin="9999"))

        assert exc_info.value.code == AuthErrorCode.INVALID_CREDENTIALS

    async def test_login_locked_account(self, service, staff_repo):
        locked_until = datetime.now(UTC) + timedelta(minutes=10)
        staff_repo.get_by_employee_id.return_value = _make_staff(locked_until=locked_until)

        with pytest.raises(AccountLockedException):
            await service.login(_make_request())

    async def test_login_resets_failed_attempts_on_success(self, service, staff_repo):
        staff_repo.get_by_employee_id.return_value = _make_staff(failed_attempts=2)

        with patch("app.services.auth_service.verify_password", return_value=True):
            await service.login(_make_request())

        staff_repo.reset_failed_attempts.assert_called_once_with("EMP001")

    async def test_login_property_network_detected(self, service, staff_repo):
        staff_repo.get_by_employee_id.return_value = _make_staff()

        with patch("app.services.auth_service.verify_password", return_value=True):
            result = await service.login(_make_request(property_network_id="PROP-HSG-001"))

        assert result.property_network.detected is True
        assert result.property_network.secure_protocol is True
