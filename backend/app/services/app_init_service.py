"""
app/services/app_init_service.py
Business logic for the splash screen / system health check.
"""

from app.core.config import get_settings
from app.core.constants import ServiceStatus
from app.schemas.shared.app_init import (
    AppInitResponse,
    FeatureFlags,
    StatusMessage,
    SystemCheck,
    SystemChecksResponse,
)

settings = get_settings()

MIN_SUPPORTED_VERSION = "1.0.0"


class AppInitService:
    async def get_init(self) -> AppInitResponse:
        return AppInitResponse(
            app_version=settings.app_version,
            min_supported_version=MIN_SUPPORTED_VERSION,
            force_update=False,
            update_url=None,
            maintenance_mode=False,
            maintenance_message=None,
            feature_flags=FeatureFlags(
                biometrics_enabled=settings.feature_biometrics_enabled,
                micro_drill_enabled=settings.feature_micro_drill_enabled,
                live_map_enabled=settings.feature_live_map_enabled,
            ),
            status_messages=await self._check_service_statuses(),
        )

    async def get_system_checks(self, user_type: str) -> SystemChecksResponse:
        checks = [
            SystemCheck(
                key="pms_connection",
                label="Property Management System",
                status=ServiceStatus.ACTIVE,
                required=True,
            ),
            SystemCheck(
                key="gps_tracking",
                label="GPS Tracking",
                status=ServiceStatus.ACTIVE,
                required=False,
            ),
            SystemCheck(
                key="radio_freq",
                label="Radio Frequency",
                status=ServiceStatus.ACTIVE,
                required=False,
            ),
            SystemCheck(
                key="property_network",
                label="Property Network",
                status=ServiceStatus.SYNCED,
                required=True,
            ),
            SystemCheck(
                key="ems_link",
                label="Emergency Services Link",
                status=ServiceStatus.ACTIVE,
                required=True,
            ),
        ]

        all_critical_passed = all(
            c.status in (ServiceStatus.ACTIVE, ServiceStatus.SYNCED)
            for c in checks
            if c.required
        )

        next_route = (
            f"/{user_type}/home" if all_critical_passed else f"/{user_type}/degraded"
        )

        return SystemChecksResponse(
            checks=checks,
            all_critical_passed=all_critical_passed,
            next_route=next_route,
        )

    async def _check_service_statuses(self) -> list[StatusMessage]:
        """
        In production this would ping real downstream services.
        Returns synthetic statuses for now.
        """
        return [
            StatusMessage(
                key="pms_connection",
                label="Property Management System",
                status=ServiceStatus.ACTIVE,
            ),
            StatusMessage(
                key="gps_tracking",
                label="GPS Tracking",
                status=ServiceStatus.ACTIVE,
            ),
            StatusMessage(
                key="radio_freq",
                label="Radio Frequency",
                status=ServiceStatus.ACTIVE,
            ),
            StatusMessage(
                key="auth_service",
                label="Authentication Service",
                status=ServiceStatus.ACTIVE,
            ),
        ]
