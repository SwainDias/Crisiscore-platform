"""Unit tests for GuestHomeService."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from app.core.exceptions import NotFoundException
from app.services.guest_home_service import GuestHomeService


@pytest.fixture
def guest_repo():
    repo = MagicMock()
    repo.get_by_guest_id = AsyncMock(
        return_value={
            "guest_id": "GST001",
            "name": "Aarav",
            "property_id": "PROP-HSG-001",
            "room_id": "ROOM-A-302",
        }
    )
    repo.get_default = AsyncMock(return_value=None)
    return repo


@pytest.fixture
def property_repo():
    repo = MagicMock()
    repo.get_by_property_id = AsyncMock(return_value={"property_id": "PROP-HSG-001", "name": "Sunrise Heights"})
    return repo


@pytest.fixture
def incident_repo():
    repo = MagicMock()
    repo.list_for_property = AsyncMock(
        return_value=[
            {
                "incident_id": "INC-1",
                "title": "Smoke Alert",
                "description": "Smoke in corridor",
                "severity": "critical",
            }
        ]
    )
    return repo


@pytest.fixture
def service(guest_repo, property_repo, incident_repo):
    return GuestHomeService(guest_repo, property_repo, incident_repo)


class TestGuestHomeService:
    async def test_get_home_with_active_alert(self, service):
        result = await service.get_home("GST001")

        assert result.guest.name == "Aarav"
        assert result.active_alert.present is True
        assert result.active_alert.alert_id == "INC-1"
        assert len(result.quick_actions) >= 1

    async def test_get_home_without_incident(self, service, incident_repo):
        incident_repo.list_for_property.return_value = []

        result = await service.get_home("GST001")

        assert result.active_alert.present is False

    async def test_get_home_missing_guest_raises(self, service, guest_repo):
        guest_repo.get_by_guest_id.return_value = None
        guest_repo.get_default.return_value = None

        with pytest.raises(NotFoundException):
            await service.get_home("MISSING")
