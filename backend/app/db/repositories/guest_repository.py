"""
app/db/repositories/guest_repository.py
"""

from app.core.constants import Collection
from app.db.repositories.base_repository import BaseRepository


class GuestRepository(BaseRepository):
    collection_name = Collection.GUESTS

    async def get_by_guest_id(self, guest_id: str) -> dict | None:
        return await self.find_one({"guest_id": guest_id})

    async def get_by_room(self, property_id: str, room_id: str) -> list[dict]:
        return await self.find_many(
            {"property_id": property_id, "room_id": room_id, "checked_out": False}
        )

    async def count_tracked(self, property_id: str) -> int:
        return await self.count({"property_id": property_id, "checked_out": False})


class CheckinRepository(BaseRepository):
    collection_name = Collection.CHECKINS

    async def get_latest_for_guest(self, guest_id: str) -> dict | None:
        docs = await self.find_many(
            {"guest_id": guest_id},
            sort=[("created_at", -1)],
            limit=1,
        )
        return docs[0] if docs else None


class RoomRepository(BaseRepository):
    collection_name = Collection.ROOMS

    async def get_by_room_id(self, property_id: str, room_id: str) -> dict | None:
        return await self.find_one({"property_id": property_id, "room_id": room_id})