"""
tests/integration/test_app_init.py
Integration tests for GET /api/v1/app/init and GET /api/v1/session/system-checks.
"""

import pytest
from httpx import AsyncClient


class TestAppInit:
    async def test_init_returns_200(self, client: AsyncClient):
        resp = await client.get("/api/v1/app/init")
        assert resp.status_code == 200

    async def test_init_payload_shape(self, client: AsyncClient):
        resp = await client.get("/api/v1/app/init")
        data = resp.json()

        assert "app_version" in data
        assert "feature_flags" in data
        assert "maintenance_mode" in data
        assert isinstance(data["status_messages"], list)

    async def test_init_maintenance_mode_false_by_default(self, client: AsyncClient):
        resp = await client.get("/api/v1/app/init")
        assert resp.json()["maintenance_mode"] is False


class TestSystemChecks:
    async def test_system_checks_staff(self, client: AsyncClient):
        resp = await client.get("/api/v1/session/system-checks?user_type=staff")
        assert resp.status_code == 200
        data = resp.json()
        assert "checks" in data
        assert "all_critical_passed" in data
        assert data["next_route"].startswith("/staff")

    async def test_system_checks_guest(self, client: AsyncClient):
        resp = await client.get("/api/v1/session/system-checks?user_type=guest")
        assert resp.status_code == 200
        assert resp.json()["next_route"].startswith("/guest")

    async def test_system_checks_invalid_type(self, client: AsyncClient):
        resp = await client.get("/api/v1/session/system-checks?user_type=robot")
        assert resp.status_code == 422
