"""
app/schemas/admin/settings.py
"""

from pydantic import BaseModel

from app.core.constants import (
    AdminRole,
    DangerZoneAction,
    IncidentType,
    IntegrationCategory,
    IntegrationStatus,
    SyncSchedule,
)


# ─── Integrations ─────────────────────────────────────────────────────────────


class APIStatus(BaseModel):
    latency_ms: int
    last_synced_at: str
    sync_schedule: SyncSchedule
    sync_interval_seconds: int | None = None


class IntegrationItem(BaseModel):
    integration_id: str
    name: str
    category: IntegrationCategory
    description: str
    logo_url: str | None = None
    status: IntegrationStatus
    auto_sync: bool
    api_status: APIStatus
    metadata: dict


class IntegrationsResponse(BaseModel):
    integrations: list[IntegrationItem]


class ConfigureIntegrationRequest(BaseModel):
    auto_sync: bool
    sync_schedule: SyncSchedule
    sync_interval_seconds: int | None = None
    credentials: dict | None = None


class ConfigureIntegrationResponse(BaseModel):
    success: bool
    status: IntegrationStatus
    message: str | None = None


# ─── Users & Roles ────────────────────────────────────────────────────────────


class AdminUserEntry(BaseModel):
    user_id: str
    name: str
    email: str
    role: AdminRole
    last_login_at: str
    active: bool


class UsersRolesResponse(BaseModel):
    users: list[AdminUserEntry]


class UpdateUserRoleRequest(BaseModel):
    role: AdminRole


# ─── Protocols ────────────────────────────────────────────────────────────────


class ProtocolItem(BaseModel):
    protocol_id: str
    name: str
    incident_type: IncidentType
    steps_count: int
    last_updated_at: str
    active: bool


class ProtocolsResponse(BaseModel):
    protocols: list[ProtocolItem]


# ─── Danger Zone ──────────────────────────────────────────────────────────────


class DangerZoneRequest(BaseModel):
    action: DangerZoneAction
    confirmed_by: str
    confirmation_token: str


class DangerZoneResponse(BaseModel):
    success: bool
    message: str
