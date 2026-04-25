"""
app/db/repositories/base_repository.py

Generic async repository providing common CRUD helpers on top of Motor.
All domain repositories inherit from this class.

SWAP GUIDE
──────────
If switching databases, replace the Motor-specific calls below with the
equivalent calls for the new driver.  The public method signatures must
remain unchanged so that service classes continue to work without edits.
"""

from datetime import UTC, datetime
from typing import Any
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase


class BaseRepository:
    collection_name: str  # subclasses must declare this

    def __init__(self, db: AsyncIOMotorDatabase) -> None:  # type: ignore[type-arg]
        self._col: AsyncIOMotorCollection = db[self.collection_name]  # type: ignore[type-arg]

    # ─── Helpers ─────────────────────────────────────────────────────────────

    @staticmethod
    def _now() -> datetime:
        return datetime.now(UTC)

    @staticmethod
    def _to_str_id(doc: dict) -> dict:
        """Convert ObjectId _id to string id for serialization."""
        if doc and "_id" in doc:
            doc["id"] = str(doc.pop("_id"))
        return doc

    # ─── CRUD ────────────────────────────────────────────────────────────────

    async def find_one(self, query: dict[str, Any]) -> dict | None:
        doc = await self._col.find_one(query)
        return self._to_str_id(doc) if doc else None

    async def find_many(
        self,
        query: dict[str, Any],
        sort: list[tuple[str, int]] | None = None,
        limit: int = 100,
        skip: int = 0,
    ) -> list[dict]:
        cursor = self._col.find(query).skip(skip).limit(limit)
        if sort:
            cursor = cursor.sort(sort)
        return [self._to_str_id(doc) async for doc in cursor]

    async def insert_one(self, data: dict[str, Any]) -> str:
        data.setdefault("created_at", self._now())
        data.setdefault("updated_at", self._now())
        result = await self._col.insert_one(data)
        return str(result.inserted_id)

    async def update_one(
        self, query: dict[str, Any], update: dict[str, Any], upsert: bool = False
    ) -> bool:
        update.setdefault("$set", {})["updated_at"] = self._now()
        result = await self._col.update_one(query, update, upsert=upsert)
        return result.modified_count > 0 or result.upserted_id is not None

    async def delete_one(self, query: dict[str, Any]) -> bool:
        result = await self._col.delete_one(query)
        return result.deleted_count > 0

    async def update_many(self, query: dict[str, Any], update: dict[str, Any]) -> int:
        update.setdefault("$set", {})["updated_at"] = self._now()
        result = await self._col.update_many(query, update)
        return int(result.modified_count)

    async def delete_many(self, query: dict[str, Any]) -> int:
        result = await self._col.delete_many(query)
        return int(result.deleted_count)

    async def count(self, query: dict[str, Any]) -> int:
        return await self._col.count_documents(query)

    async def exists(self, query: dict[str, Any]) -> bool:
        return await self.count(query) > 0
