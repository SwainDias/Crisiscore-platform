"""Unit tests for AdminSettingsService."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from app.core.exceptions import NotFoundException
from app.schemas.admin.system_settings import (
    ConfigureIntegrationRequest,
    DangerZoneRequest,
)
from app.services.admin_settings_service import AdminSettingsService


@pytest.fixture
def settings_repo():
    repo = MagicMock()
    repo.get_by_key = AsyncMock(return_value={"key": "general", "settings": {"default_language": "en"}})
    repo.update_one = AsyncMock(return_value=True)
    return repo


@pytest.fixture
def integration_repo():
    repo = MagicMock()
    repo.list_all = AsyncMock(return_value=[])
    repo.get_by_integration_id = AsyncMock(return_value=None)
    repo.update_one = AsyncMock(return_value=True)
    return repo


@pytest.fixture
def user_role_repo():
    repo = MagicMock()
    repo.list_users = AsyncMock(return_value=[])
    repo.update_one = AsyncMock(return_value=True)
    return repo


@pytest.fixture
def protocol_repo():
    repo = MagicMock()
    repo.list_protocols = AsyncMock(return_value=[])
    return repo


@pytest.fixture
def incident_repo():
    repo = MagicMock()
    repo.resolve_all_active = AsyncMock(return_value=2)
    return repo


@pytest.fixture
def guest_repo():
    repo = MagicMock()
    repo.delete_many = AsyncMock(return_value=3)
    return repo


@pytest.fixture
def checkin_repo():
    repo = MagicMock()
    repo.delete_many = AsyncMock(return_value=2)
    return repo


@pytest.fixture
def service(
    settings_repo,
    integration_repo,
    user_role_repo,
    protocol_repo,
    incident_repo,
    guest_repo,
    checkin_repo,
):
    return AdminSettingsService(
        settings_repo=settings_repo,
        integration_repo=integration_repo,
        user_role_repo=user_role_repo,
        protocol_repo=protocol_repo,
        incident_repo=incident_repo,
        guest_repo=guest_repo,
        checkin_repo=checkin_repo,
    )


class TestAdminSettingsService:
    async def test_list_integrations_uses_defaults_when_empty(self, service):
        result = await service.list_integrations()
        assert len(result.integrations) >= 1

    async def test_configure_integration_not_found(self, service):
        payload = ConfigureIntegrationRequest(
            auto_sync=True,
            sync_schedule="manual",
            sync_interval_seconds=None,
            credentials={"api_key": "secret"},
        )

        with pytest.raises(NotFoundException):
            await service.configure_integration("missing", payload)

    async def test_danger_zone_clear_guest_registry(self, service):
        payload = DangerZoneRequest(
            action="clear_guest_registry",
            confirmed_by="ADM001",
            confirmation_token="token",
        )

        result = await service.danger_zone("clear_guest_registry", payload)

        assert result.success is True
        assert "Cleared guest registry" in result.message
