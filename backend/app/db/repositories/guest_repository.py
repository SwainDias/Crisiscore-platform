"""
app/db/repositories/guest_repository.py
"""

from pymongo import DESCENDING

from app.core.constants import Collection
from app.db.repositories.base_repository import BaseRepository


class GuestRepository(BaseRepository):
    collection_name = Collection.GUESTS

    async def get_by_guest_id(self, guest_id: str) -> dict | None:
        return await self.find_one({"guest_id": guest_id})

    async def get_default(self) -> dict | None:
        docs = await self.find_many({}, limit=1)
        return docs[0] if docs else None

    async def list_for_property(self, property_id: str, limit: int = 500) -> list[dict]:
        return await self.find_many(
            {"property_id": property_id},
            sort=[("name", 1)],
            limit=limit,
        )

    async def count_tracked(self, property_id: str) -> int:
        return await self.count({"property_id": property_id})

    async def upsert_emergency_profile(
        self,
        guest_id: str,
        room_id: str,
        emergency_profile: dict,
    ) -> bool:
        return await self.update_one(
            {"guest_id": guest_id},
            {
                "$set": {
                    "room_id": room_id,
                    "emergency_profile": emergency_profile,
                }
            },
            upsert=True,
        )


class RoomRepository(BaseRepository):
    collection_name = Collection.ROOMS

    async def get_by_room_id(self, room_id: str) -> dict | None:
        return await self.find_one({"room_id": room_id})

    async def list_floors(self, property_id: str) -> list[int]:
        rows = await self.find_many(
            {"property_id": property_id},
            sort=[("floor", 1)],
            limit=500,
        )
        floors: list[int] = sorted({int(r.get("floor", 0)) for r in rows if r.get("floor") is not None})
        return floors

    async def list_for_floor(self, property_id: str, floor: int) -> list[dict]:
        return await self.find_many(
            {"property_id": property_id, "floor": floor},
            sort=[("room_number", 1)],
            limit=500,
        )


class GuestCheckinRepository(BaseRepository):
    collection_name = Collection.GUEST_CHECKINS

    async def get_latest_for_guest(self, guest_id: str) -> dict | None:
        docs = await self.find_many(
            {"guest_id": guest_id},
            sort=[("created_at", DESCENDING)],
            limit=1,
        )
        return docs[0] if docs else None

    async def get_by_checkin_id(self, checkin_id: str) -> dict | None:
        return await self.find_one({"checkin_id": checkin_id})
