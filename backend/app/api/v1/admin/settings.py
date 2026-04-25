"""
app/api/v1/admin/settings.py
"""

from fastapi import APIRouter, Depends

from app.core.dependencies import AdminOnly, DBDep
from app.db.repositories.admin_repository import (
    IntegrationRepository,
    ProtocolRepository,
    SettingsRepository,
    UserRoleRepository,
)
from app.db.repositories.guest_repository import GuestCheckinRepository, GuestRepository
from app.db.repositories.incident_command_repository import IncidentCommandRepository
from app.schemas.admin.system_settings import (
    AdminSettingsResponse,
    ConfigureIntegrationRequest,
    ConfigureIntegrationResponse,
    DangerZoneRequest,
    DangerZoneResponse,
    IntegrationsResponse,
    ProtocolsResponse,
    UpdateGeneralSettingsRequest,
    UpdateUserRoleRequest,
    UpdateUserRoleResponse,
    UsersRolesResponse,
)
from app.services.admin_settings_service import AdminSettingsService

router = APIRouter(prefix="/admin/settings", tags=["Admin — System Settings"])


def _get_service(db: DBDep) -> AdminSettingsService:
    return AdminSettingsService(
        settings_repo=SettingsRepository(db),
        integration_repo=IntegrationRepository(db),
        user_role_repo=UserRoleRepository(db),
        protocol_repo=ProtocolRepository(db),
        incident_repo=IncidentCommandRepository(db),
        guest_repo=GuestRepository(db),
        checkin_repo=GuestCheckinRepository(db),
    )


@router.get(
    "",
    response_model=AdminSettingsResponse,
    summary="Get General Settings",
)
async def get_settings(
    current_staff: dict = AdminOnly,
    service: AdminSettingsService = Depends(_get_service),
) -> AdminSettingsResponse:
    return await service.get_settings()


@router.patch(
    "/general",
    response_model=AdminSettingsResponse,
    summary="Update General Settings",
)
async def update_general(
    payload: UpdateGeneralSettingsRequest,
    current_staff: dict = AdminOnly,
    service: AdminSettingsService = Depends(_get_service),
) -> AdminSettingsResponse:
    return await service.update_general(payload)


@router.get(
    "/integrations",
    response_model=IntegrationsResponse,
    summary="List Integrations",
)
async def list_integrations(
    current_staff: dict = AdminOnly,
    service: AdminSettingsService = Depends(_get_service),
) -> IntegrationsResponse:
    return await service.list_integrations()


@router.patch(
    "/integrations/{integration_id}",
    response_model=ConfigureIntegrationResponse,
    summary="Configure Integration",
)
async def configure_integration(
    integration_id: str,
    payload: ConfigureIntegrationRequest,
    current_staff: dict = AdminOnly,
    service: AdminSettingsService = Depends(_get_service),
) -> ConfigureIntegrationResponse:
    return await service.configure_integration(integration_id, payload)


@router.post(
    "/integrations/{integration_id}/toggle",
    response_model=ConfigureIntegrationResponse,
    summary="Toggle Integration",
)
async def toggle_integration(
    integration_id: str,
    current_staff: dict = AdminOnly,
    service: AdminSettingsService = Depends(_get_service),
) -> ConfigureIntegrationResponse:
    return await service.toggle_integration(integration_id)


@router.get(
    "/users",
    response_model=UsersRolesResponse,
    summary="List Users & Roles",
)
async def list_users_roles(
    current_staff: dict = AdminOnly,
    service: AdminSettingsService = Depends(_get_service),
) -> UsersRolesResponse:
    return await service.list_users_roles()


@router.patch(
    "/users/{user_id}/role",
    response_model=UpdateUserRoleResponse,
    summary="Update User Role",
)
async def update_user_role(
    user_id: str,
    payload: UpdateUserRoleRequest,
    current_staff: dict = AdminOnly,
    service: AdminSettingsService = Depends(_get_service),
) -> UpdateUserRoleResponse:
    return await service.update_user_role(user_id, payload)


@router.get(
    "/protocols",
    response_model=ProtocolsResponse,
    summary="List Incident Protocols",
)
async def list_protocols(
    current_staff: dict = AdminOnly,
    service: AdminSettingsService = Depends(_get_service),
) -> ProtocolsResponse:
    return await service.list_protocols()


@router.post(
    "/danger/{action}",
    response_model=DangerZoneResponse,
    summary="Danger Zone Operation",
)
async def danger_zone(
    action: str,
    payload: DangerZoneRequest,
    current_staff: dict = AdminOnly,
    service: AdminSettingsService = Depends(_get_service),
) -> DangerZoneResponse:
    return await service.danger_zone(action, payload)
