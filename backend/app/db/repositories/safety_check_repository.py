"""
app/db/repositories/safety_check_repository.py
"""

from bson import ObjectId
from pymongo import DESCENDING

from app.core.constants import Collection
from app.db.repositories.base_repository import BaseRepository


class SafetyCheckRepository(BaseRepository):
    collection_name = Collection.SAFETY_CHECKS

    async def get_latest_for_staff(self, employee_id: str) -> dict | None:
        docs = await self.find_many(
            {"employee_id": employee_id},
            sort=[("generated_at", DESCENDING)],
            limit=1,
        )
        return docs[0] if docs else None

    async def get_by_check_id(self, check_id: str) -> dict | None:
        try:
            oid = ObjectId(check_id)
        except Exception:
            return None
        return await self.find_one({"_id": oid})

    async def confirm(self, check_id: str, confirmed_at, override_note: str | None) -> bool:
        try:
            oid = ObjectId(check_id)
        except Exception:
            return False
        return await self.update_one(
            {"_id": oid},
            {"$set": {"confirmed_at": confirmed_at, "override_note": override_note}},
        )
