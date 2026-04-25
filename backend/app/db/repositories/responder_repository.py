"""
app/db/repositories/responder_repository.py
"""

from pymongo import ASCENDING

from app.core.constants import Collection
from app.db.repositories.base_repository import BaseRepository


class ResponderLogRepository(BaseRepository):
    collection_name = Collection.RESPONDER_LOGS

    async def list_for_incident(self, incident_id: str) -> list[dict]:
        return await self.find_many(
            {"incident_id": incident_id},
            sort=[("created_at", ASCENDING)],
        )

    async def append_log(self, incident_id: str, responder_id: str, note: str, timestamp) -> str:
        return await self.insert_one(
            {
                "incident_id": incident_id,
                "responder_id": responder_id,
                "note": note,
                "logged_at": timestamp,
            }
        )


class SOPRepository(BaseRepository):
    collection_name = Collection.SOP_PROTOCOLS

    async def get_for_incident_type(self, incident_type: str) -> dict | None:
        return await self.find_one({"incident_type": incident_type, "active": True})

    async def get_by_id(self, protocol_id: str) -> dict | None:
        from bson import ObjectId
        try:
            oid = ObjectId(protocol_id)
        except Exception:
            return None
        return await self.find_one({"_id": oid})

    async def list_all(self) -> list[dict]:
        return await self.find_many({})