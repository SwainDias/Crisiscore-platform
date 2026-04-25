"""
app/db/repositories/task_repository.py
"""

from pymongo import ASCENDING, DESCENDING

from app.core.constants import Collection, TaskStatus
from app.db.repositories.base_repository import BaseRepository


class TaskRepository(BaseRepository):
    collection_name = Collection.TASKS

    async def list_for_staff(
        self, employee_id: str, limit: int = 20
    ) -> list[dict]:
        return await self.find_many(
            {
                "assigned_to": employee_id,
                "status": {"$ne": TaskStatus.COMPLETED},
            },
            sort=[("priority_order", ASCENDING), ("due_at", ASCENDING)],
            limit=limit,
        )

    async def count_for_staff(self, employee_id: str) -> int:
        return await self.count({"assigned_to": employee_id})
