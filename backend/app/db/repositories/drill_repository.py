"""
app/db/repositories/drill_repository.py
"""

from bson import ObjectId
from pymongo import ASCENDING

from app.core.constants import Collection
from app.db.repositories.base_repository import BaseRepository


class DrillRepository(BaseRepository):
    collection_name = Collection.DRILLS

    async def get_by_drill_id(self, drill_id: str) -> dict | None:
        return await self.find_one({"drill_id": drill_id})


class DrillQuestionRepository(BaseRepository):
    collection_name = Collection.DRILL_QUESTIONS

    async def list_for_drill(self, drill_id: str) -> list[dict]:
        return await self.find_many(
            {"drill_id": drill_id},
            sort=[("index", ASCENDING)],
        )

    async def get_by_question_id(self, question_id: str) -> dict | None:
        return await self.find_one({"question_id": question_id})


class DrillSessionRepository(BaseRepository):
    collection_name = Collection.DRILL_SESSIONS

    async def get_by_session_id(self, session_id: str) -> dict | None:
        try:
            oid = ObjectId(session_id)
        except Exception:
            return None
        return await self.find_one({"_id": oid})

    async def append_answer(self, session_id: str, answer: dict) -> bool:
        try:
            oid = ObjectId(session_id)
        except Exception:
            return False
        result = await self._col.update_one(
            {"_id": oid},
            {
                "$push": {"answers": answer},
                "$set": {"updated_at": self._now()},
            },
        )
        return result.modified_count > 0
