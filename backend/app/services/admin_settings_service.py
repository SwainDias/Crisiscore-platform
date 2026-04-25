"""
app/services/admin_settings_service.py
"""

from datetime import UTC, datetime

from app.core.constants import DangerZoneAction, IntegrationStatus
from app.core.exceptions import NotFoundException
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
    IntegrationApiStatus,
    IntegrationItem,
    IntegrationMetadata,
    IntegrationsResponse,
    ProtocolItem,
    ProtocolsResponse,
    UpdateGeneralSettingsRequest,
    UpdateUserRoleRequest,
    UpdateUserRoleResponse,
    UserRoleItem,
    UsersRolesResponse,
)


class AdminSettingsService:
    def __init__(
        self,
        settings_repo: SettingsRepository,
        integration_repo: IntegrationRepository,
        user_role_repo: UserRoleRepository,
        protocol_repo: ProtocolRepository,
        incident_repo: IncidentCommandRepository,
        guest_repo: GuestRepository,
        checkin_repo: GuestCheckinRepository,
    ) -> None:
        self._settings_repo = settings_repo
        self._integration_repo = integration_repo
        self._user_role_repo = user_role_repo
        self._protocol_repo = protocol_repo
        self._incident_repo = incident_repo
        self._guest_repo = guest_repo
        self._checkin_repo = checkin_repo

    async def get_settings(self) -> AdminSettingsResponse:
        doc = await self._settings_repo.get_by_key("general")
        settings = (doc or {}).get(
            "settings",
            {
                "auto_dispatch_enabled": True,
                "default_language": "en",
                "guest_tracking_opt_in": True,
                "drill_frequency_days": 7,
            },
        )
        return AdminSettingsResponse(settings=settings)

    async def update_general(self, request: UpdateGeneralSettingsRequest) -> AdminSettingsResponse:
        await self._settings_repo.update_one(
            {"key": "general"},
            {"$set": {"settings": request.settings}},
            upsert=True,
        )
        return AdminSettingsResponse(settings=request.settings)

    async def list_integrations(self) -> IntegrationsResponse:
        docs = await self._integration_repo.list_all()
        if not docs:
            docs = self._default_integrations()

        return IntegrationsResponse(
            integrations=[self._to_integration_item(doc) for doc in docs]
        )

    async def configure_integration(
        self,
        integration_id: str,
        request: ConfigureIntegrationRequest,
    ) -> ConfigureIntegrationResponse:
        existing = await self._integration_repo.get_by_integration_id(integration_id)
        if not existing:
            raise NotFoundException(message=f"Integration '{integration_id}' not found.")

        credential_keys = sorted(list(request.credentials.keys()))
        await self._integration_repo.update_one(
            {"integration_id": integration_id},
            {
                "$set": {
                    "auto_sync": request.auto_sync,
                    "api_status.sync_schedule": request.sync_schedule,
                    "api_status.sync_interval_seconds": request.sync_interval_seconds,
                    "credential_keys": credential_keys,
                    "status": IntegrationStatus.CONNECTED,
                    "api_status.last_synced_at": datetime.now(UTC).isoformat(),
                }
            },
        )

        return ConfigureIntegrationResponse(
            success=True,
            status=IntegrationStatus.CONNECTED,
            message=None,
        )

    async def toggle_integration(self, integration_id: str) -> ConfigureIntegrationResponse:
        existing = await self._integration_repo.get_by_integration_id(integration_id)
        if not existing:
            raise NotFoundException(message=f"Integration '{integration_id}' not found.")

        current = existing.get("status", IntegrationStatus.DISCONNECTED)
        next_status = (
            IntegrationStatus.DISCONNECTED
            if current == IntegrationStatus.CONNECTED
            else IntegrationStatus.CONNECTED
        )

        await self._integration_repo.update_one(
            {"integration_id": integration_id},
            {"$set": {"status": next_status}},
        )

        return ConfigureIntegrationResponse(
            success=True,
            status=next_status,
            message=f"Integration {next_status}.",
        )

    async def list_users_roles(self) -> UsersRolesResponse:
        rows = await self._user_role_repo.list_users()
        return UsersRolesResponse(
            users=[
                UserRoleItem(
                    user_id=row.get("user_id", ""),
                    name=row.get("name", "User"),
                    email=row.get("email", ""),
                    role=row.get("role", "responder"),
                    last_login_at=row.get("last_login_at", datetime.now(UTC).isoformat()),
                    active=bool(row.get("active", True)),
                )
                for row in rows
            ]
        )

    async def update_user_role(
        self,
        user_id: str,
        request: UpdateUserRoleRequest,
    ) -> UpdateUserRoleResponse:
        await self._user_role_repo.update_one(
            {"user_id": user_id},
            {"$set": {"role": request.role, "active": True}},
            upsert=True,
        )
        return UpdateUserRoleResponse(success=True, user_id=user_id, role=request.role)

    async def list_protocols(self) -> ProtocolsResponse:
        docs = await self._protocol_repo.list_protocols()
        return ProtocolsResponse(
            protocols=[
                ProtocolItem(
                    protocol_id=d.get("protocol_id", ""),
                    name=d.get("name", "Protocol"),
                    incident_type=d.get("incident_type", "custom"),
                    steps_count=int(d.get("steps_count", 0)),
                    last_updated_at=d.get("last_updated_at", datetime.now(UTC).isoformat()),
                    active=bool(d.get("active", True)),
                )
                for d in docs
            ]
        )

    async def danger_zone(self, action: str, request: DangerZoneRequest) -> DangerZoneResponse:
        if action != request.action:
            return DangerZoneResponse(success=False, message="Action mismatch in request.")

        if request.action == DangerZoneAction.RESET_ALL_INCIDENTS:
            modified = await self._incident_repo.resolve_all_active()
            return DangerZoneResponse(success=True, message=f"Resolved {modified} active incidents.")

        if request.action == DangerZoneAction.CLEAR_GUEST_REGISTRY:
            deleted_guests = await self._guest_repo.delete_many({})
            deleted_checkins = await self._checkin_repo.delete_many({})
            return DangerZoneResponse(
                success=True,
                message=f"Cleared guest registry ({deleted_guests} guests, {deleted_checkins} check-ins).",
            )

        if request.action == DangerZoneAction.FACTORY_RESET:
            modified = await self._incident_repo.resolve_all_active()
            deleted_guests = await self._guest_repo.delete_many({})
            deleted_checkins = await self._checkin_repo.delete_many({})
            return DangerZoneResponse(
                success=True,
                message=(
                    "Factory reset complete: "
                    f"resolved {modified} incidents, removed {deleted_guests} guests, "
                    f"removed {deleted_checkins} check-ins."
                ),
            )

        return DangerZoneResponse(success=False, message="Unsupported danger-zone action.")

    def _to_integration_item(self, doc: dict) -> IntegrationItem:
        api_status_doc = doc.get("api_status", {})
        metadata_doc = doc.get("metadata", {})

        metadata_items: list[IntegrationMetadata] = []
        if isinstance(metadata_doc, dict):
            metadata_items = [
                IntegrationMetadata(key=k, value=v)
                for k, v in metadata_doc.items()
                if isinstance(v, (str, int, bool))
            ]

        return IntegrationItem(
            integration_id=doc.get("integration_id", ""),
            name=doc.get("name", "Integration"),
            category=doc.get("category", "communication"),
            description=doc.get("description", ""),
            logo_url=doc.get("logo_url"),
            status=doc.get("status", IntegrationStatus.DISCONNECTED),
            auto_sync=bool(doc.get("auto_sync", False)),
            api_status=IntegrationApiStatus(
                latency_ms=int(api_status_doc.get("latency_ms", 0)),
                last_synced_at=api_status_doc.get("last_synced_at", datetime.now(UTC).isoformat()),
                sync_schedule=api_status_doc.get("sync_schedule", "manual"),
                sync_interval_seconds=api_status_doc.get("sync_interval_seconds"),
            ),
            metadata=metadata_items,
        )

    @staticmethod
    def _default_integrations() -> list[dict]:
        now = datetime.now(UTC).isoformat()
        return [
            {
                "integration_id": "int-whatsapp",
                "name": "WhatsApp Business",
                "category": "communication",
                "description": "Guest broadcast channel",
                "status": "connected",
                "auto_sync": True,
                "api_status": {
                    "latency_ms": 124,
                    "last_synced_at": now,
                    "sync_schedule": "real_time_webhook",
                    "sync_interval_seconds": None,
                },
                "metadata": {"region": "ap-south-1"},
            },
            {
                "integration_id": "int-cctv",
                "name": "CCTV Grid",
                "category": "physical_security",
                "description": "Live camera synchronization",
                "status": "disconnected",
                "auto_sync": False,
                "api_status": {
                    "latency_ms": 0,
                    "last_synced_at": now,
                    "sync_schedule": "manual",
                    "sync_interval_seconds": None,
                },
                "metadata": {"streams": 0},
            },
        ]
