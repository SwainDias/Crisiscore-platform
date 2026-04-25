"""
app/schemas/shared/app_init.py
"""

from pydantic import BaseModel

from app.core.constants import ServiceStatus


class FeatureFlags(BaseModel):
    biometrics_enabled: bool
    micro_drill_enabled: bool
    live_map_enabled: bool


class StatusMessage(BaseModel):
    key: str
    label: str
    status: ServiceStatus


class AppInitResponse(BaseModel):
    app_version: str
    min_supported_version: str
    force_update: bool
    update_url: str | None = None
    maintenance_mode: bool
    maintenance_message: str | None = None
    feature_flags: FeatureFlags
    status_messages: list[StatusMessage]


class SystemCheck(BaseModel):
    key: str
    label: str
    status: ServiceStatus
    required: bool


class SystemChecksResponse(BaseModel):
    checks: list[SystemCheck]
    all_critical_passed: bool
    next_route: str
