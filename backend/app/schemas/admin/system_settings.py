"""
app/schemas/admin/system_settings.py
"""

from typing import Literal

from pydantic import BaseModel

from app.core.constants import (
    AdminUserRole,
    DangerZoneAction,
    IncidentType,
    IntegrationCategory,
    IntegrationStatus,
    SyncSchedule,
)


class AdminSettingsResponse(BaseModel):
    settings: dict[str, str | int | bool | None]


class UpdateGeneralSettingsRequest(BaseModel):
    settings: dict[str, str | int | bool | None]


class IntegrationApiStatus(BaseModel):
    latency_ms: int
    last_synced_at: str
    sync_schedule: SyncSchedule
    sync_interval_seconds: int | None = None


class IntegrationMetadata(BaseModel):
    key: str
    value: str | int | bool


class IntegrationItem(BaseModel):
    integration_id: str
    name: str
    category: IntegrationCategory
    description: str
    logo_url: str | None = None
    status: IntegrationStatus
    auto_sync: bool
    api_status: IntegrationApiStatus
    metadata: list[IntegrationMetadata]


class IntegrationsResponse(BaseModel):
    integrations: list[IntegrationItem]


class ConfigureIntegrationRequest(BaseModel):
    auto_sync: bool
    sync_schedule: SyncSchedule
    sync_interval_seconds: int | None = None
    credentials: dict[str, str]


class ConfigureIntegrationResponse(BaseModel):
    success: bool
    status: Literal[IntegrationStatus.CONNECTED, IntegrationStatus.ERROR]
    message: str | None = None


class UserRoleItem(BaseModel):
    user_id: str
    name: str
    email: str
    role: AdminUserRole
    last_login_at: str
    active: bool


class UsersRolesResponse(BaseModel):
    users: list[UserRoleItem]


class UpdateUserRoleRequest(BaseModel):
    role: AdminUserRole


class UpdateUserRoleResponse(BaseModel):
    success: bool
    user_id: str
    role: AdminUserRole


class ProtocolItem(BaseModel):
    protocol_id: str
    name: str
    incident_type: IncidentType
    steps_count: int
    last_updated_at: str
    active: bool


class ProtocolsResponse(BaseModel):
    protocols: list[ProtocolItem]


class DangerZoneRequest(BaseModel):
    action: DangerZoneAction
    confirmed_by: str
    confirmation_token: str


class DangerZoneResponse(BaseModel):
    success: bool
    message: str
