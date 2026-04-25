"""
app/db/repositories/alert_repository.py
"""

from datetime import UTC, datetime, timedelta
from pymongo import DESCENDING

from app.core.constants import Collection
from app.db.repositories.base_repository import BaseRepository


class AlertRepository(BaseRepository):
    collection_name = Collection.ALERTS

    async def get_by_alert_id(self, alert_id: str) -> dict | None:
        return await self.find_one({"alert_id": alert_id})

    async def get_recent_duplicate(
        self, user_id: str, type_id: str, window_minutes: int = 5
    ) -> dict | None:
        """Check for a duplicate alert from the same user within `window_minutes`."""
        since = datetime.now(UTC) - timedelta(minutes=window_minutes)
        return await self.find_one(
            {
                "raised_by.user_id": user_id,
                "type_id": type_id,
                "created_at": {"$gte": since},
            }
        )

    async def list_for_incident(self, incident_id: str) -> list[dict]:
        return await self.find_many(
            {"incident_id": incident_id},
            sort=[("created_at", DESCENDING)],
        )


class AlertTypeRepository(BaseRepository):
    collection_name = Collection.ALERT_TYPES

    async def get_all_active(self) -> list[dict]:
        return await self.find_many({"active": True})

    async def get_by_type_id(self, type_id: str) -> dict | None:
        return await self.find_one({"type_id": type_id})
