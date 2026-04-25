"""
app/db/repositories/incident_repository.py
"""

from pymongo import DESCENDING

from app.core.constants import Collection, IncidentStatus
from app.db.repositories.base_repository import BaseRepository


class IncidentRepository(BaseRepository):
    collection_name = Collection.INCIDENTS

    async def get_active_for_property(self, property_id: str) -> dict | None:
        return await self.find_one(
            {"property_id": property_id, "status": IncidentStatus.ACTIVE}
        )

    async def get_by_id(self, incident_id: str) -> dict | None:
        from bson import ObjectId
        try:
            oid = ObjectId(incident_id)
        except Exception:
            return None
        return await self.find_one({"_id": oid})

    async def get_resolved_by_id(self, incident_id: str) -> dict | None:
        from bson import ObjectId
        try:
            oid = ObjectId(incident_id)
        except Exception:
            return None
        return await self.find_one({"_id": oid, "status": IncidentStatus.RESOLVED})

    async def list_for_property(
        self, property_id: str, limit: int = 20, skip: int = 0
    ) -> list[dict]:
        return await self.find_many(
            {"property_id": property_id},
            sort=[("created_at", DESCENDING)],
            limit=limit,
            skip=skip,
        )

    async def resolve(self, incident_id: str, concluded_at) -> bool:
        from bson import ObjectId
        return await self.update_one(
            {"_id": ObjectId(incident_id)},
            {"$set": {"status": IncidentStatus.RESOLVED, "concluded_at": concluded_at}},
        )
