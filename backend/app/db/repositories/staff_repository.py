"""
app/db/repositories/staff_repository.py
"""

from app.core.constants import Collection
from app.db.repositories.base_repository import BaseRepository


class StaffRepository(BaseRepository):
    collection_name = Collection.STAFF

    async def get_by_employee_id(self, employee_id: str) -> dict | None:
        return await self.find_one({"employee_id": employee_id})

    async def increment_failed_attempts(self, employee_id: str) -> int:
        """Atomically increments and returns new failed_attempts count."""
        result = await self._col.find_one_and_update(
            {"employee_id": employee_id},
            {"$inc": {"failed_attempts": 1}, "$set": {"updated_at": self._now()}},
            return_document=True,
        )
        return result["failed_attempts"] if result else 0

    async def reset_failed_attempts(self, employee_id: str) -> None:
        await self.update_one(
            {"employee_id": employee_id},
            {"$set": {"failed_attempts": 0, "locked_until": None}},
        )

    async def lock_account(self, employee_id: str, locked_until) -> None:
        await self.update_one(
            {"employee_id": employee_id},
            {"$set": {"locked_until": locked_until}},
        )

    async def update_last_login(self, employee_id: str, device_id: str) -> None:
        await self.update_one(
            {"employee_id": employee_id},
            {"$set": {"last_login_at": self._now(), "last_device_id": device_id}},
        )
