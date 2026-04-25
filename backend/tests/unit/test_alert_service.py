"""
tests/unit/test_alert_service.py
Unit tests for AlertService.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from app.core.exceptions import DuplicateAlertException, NotFoundException
from app.schemas.shared.alert import RaiseAlertRequest, RaisedBy
from app.schemas.shared.base import LocationSchema
from app.services.alert_service import AlertService


def _make_request(**overrides) -> RaiseAlertRequest:
    base = {
        "type_id": "FIRE",
        "additional_details": "Smoke on 3rd floor",
        "location": LocationSchema(lat=19.076, lng=72.877),
        "raised_by": RaisedBy(user_type="staff", user_id="EMP001"),
        "device_id": "DEV-001",
        "timestamp": "2025-01-01T10:00:00+00:00",
    }
    base.update(overrides)
    return RaiseAlertRequest(**base)


def _fire_type() -> dict:
    return {
        "type_id": "FIRE",
        "label": "Fire",
        "description": "Fire emergency",
        "icon": "flame",
        "color_hex": "#FF4500",
        "severity_default": "critical",
        "active": True,
    }


@pytest.fixture
def alert_repo():
    repo = MagicMock()
    repo.get_recent_duplicate = AsyncMock(return_value=None)
    repo.insert_one = AsyncMock(return_value="some-id")
    return repo


@pytest.fixture
def alert_type_repo():
    repo = MagicMock()
    repo.get_all_active = AsyncMock(return_value=[_fire_type()])
    repo.get_by_type_id = AsyncMock(return_value=_fire_type())
    return repo


@pytest.fixture
def incident_repo():
    repo = MagicMock()
    repo.get_active_for_property = AsyncMock(return_value=None)
    repo.insert_one = AsyncMock(return_value="incident-id")
    return repo


@pytest.fixture
def service(alert_repo, alert_type_repo, incident_repo):
    return AlertService(alert_repo, alert_type_repo, incident_repo)


class TestRaiseAlert:
    async def test_raise_alert_success(self, service, alert_repo):
        result = await service.raise_alert(_make_request())

        assert result.success is True
        assert result.alert_id != ""
        assert result.responders_notified > 0

    async def test_raise_alert_unknown_type(self, service, alert_type_repo):
        alert_type_repo.get_by_type_id.return_value = None

        with pytest.raises(NotFoundException):
            await service.raise_alert(_make_request(type_id="UNKNOWN"))

    async def test_raise_alert_duplicate_blocked(self, service, alert_repo):
        alert_repo.get_recent_duplicate.return_value = {"alert_id": "existing"}

        with pytest.raises(DuplicateAlertException):
            await service.raise_alert(_make_request())

    async def test_get_alert_types(self, service):
        result = await service.get_alert_types()

        assert len(result.types) == 1
        assert result.types[0].type_id == "FIRE"


class TestAttachToIncident:
    async def test_critical_alert_creates_incident(self, service, incident_repo):
        incident_repo.get_active_for_property.return_value = None

        result = await service.raise_alert(_make_request())

        # A new incident should have been created
        incident_repo.insert_one.assert_called_once()
        assert result.incident_id is not None

    async def test_critical_alert_reuses_existing_incident(self, service, incident_repo):
        incident_repo.get_active_for_property.return_value = {"id": "EXISTING-INC"}

        result = await service.raise_alert(_make_request())

        # insert_one should NOT have been called for the incident
        incident_repo.insert_one.assert_not_called()
        assert result.incident_id == "EXISTING-INC"
