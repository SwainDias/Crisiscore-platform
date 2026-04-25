"""
app/db/repositories/action_item_repository.py
"""

from app.core.constants import Collection
from app.db.repositories.base_repository import BaseRepository


class ActionItemRepository(BaseRepository):
    collection_name = Collection.ACTION_ITEMS

    async def list_for_incident(self, incident_id: str) -> list[dict]:
        return await self.find_many({"incident_id": incident_id})
