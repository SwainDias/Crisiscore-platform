"""
app/db/repositories/admin_repository.py
"""

import uuid
from pymongo import DESCENDING

from app.core.constants import Collection
from app.db.repositories.base_repository import BaseRepository


class BroadcastRepository(BaseRepository):
    collection_name = Collection.BROADCASTS

    async def list_for_incident(self, incident_id: str, limit: int = 20) -> list[dict]:
        return await self.find_many(
            {"incident_id": incident_id},
            sort=[("created_at", DESCENDING)],
            limit=limit,
        )


class IntegrationRepository(BaseRepository):
    collection_name = Collection.INTEGRATIONS

    async def list_for_property(self, property_id: str) -> list[dict]:
        return await self.find_many({"property_id": property_id})

    async def get_by_integration_id(
        self, property_id: str, integration_id: str
    ) -> dict | None:
        return await self.find_one(
            {"property_id": property_id, "integration_id": integration_id}
        )

    async def toggle(self, property_id: str, integration_id: str, enabled: bool) -> bool:
        return await self.update_one(
            {"property_id": property_id, "integration_id": integration_id},
            {"$set": {"enabled": enabled}},
        )


class AdminUserRepository(BaseRepository):
    collection_name = Collection.ADMIN_USERS

    async def get_by_user_id(self, user_id: str) -> dict | None:
        return await self.find_one({"user_id": user_id})

    async def list_for_property(self, property_id: str) -> list[dict]:
        return await self.find_many({"property_id": property_id})

    async def update_role(self, user_id: str, role: str) -> bool:
        return await self.update_one(
            {"user_id": user_id},
            {"$set": {"role": role}},
        )