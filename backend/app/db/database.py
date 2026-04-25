"""
app/db/database.py

MongoDB connection management using Motor (async driver).

SWAP GUIDE
──────────
To swap to a different database (e.g., PostgreSQL + asyncpg / SQLAlchemy):
1.  Replace `_client` and `_db` with your new engine/session factory.
2.  Update `get_db()` to yield the appropriate session/connection.
3.  Re-implement the repository classes in db/repositories/ — all service
    layer code uses repositories exclusively, so no other files need changes.
"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import ASCENDING, DESCENDING
from typing import AsyncGenerator

from app.core.config import get_settings

settings = get_settings()

_client: AsyncIOMotorClient | None = None  # type: ignore[type-arg]
_db: AsyncIOMotorDatabase | None = None  # type: ignore[type-arg]


async def connect_db() -> None:
    """Called on application startup."""
    global _client, _db
    _client = AsyncIOMotorClient(
        settings.mongo_uri,
        serverSelectionTimeoutMS=5_000,
        connectTimeoutMS=5_000,
    )
    _db = _client[settings.mongo_db_name]
    await _ensure_indexes(_db)


async def disconnect_db() -> None:
    """Called on application shutdown."""
    global _client
    if _client:
        _client.close()
        _client = None


async def get_db() -> AsyncGenerator[AsyncIOMotorDatabase, None]:  # type: ignore[type-arg]
    """FastAPI dependency — yields the active DB handle."""
    if _db is None:
        raise RuntimeError("Database not initialized. Call connect_db() first.")
    yield _db


# ─── Index Definitions ───────────────────────────────────────────────────────
# Centralised here so they run once at startup and are easy to audit / extend.

async def _ensure_indexes(db: AsyncIOMotorDatabase) -> None:  # type: ignore[type-arg]
    # staff
    await db.staff.create_index([("employee_id", ASCENDING)], unique=True)
    await db.staff.create_index([("property_id", ASCENDING)])

    # incidents
    await db.incidents.create_index([("status", ASCENDING)])
    await db.incidents.create_index([("property_id", ASCENDING), ("status", ASCENDING)])
    await db.incidents.create_index([("created_at", DESCENDING)])

    # alerts
    await db.alerts.create_index([("incident_id", ASCENDING)])
    await db.alerts.create_index([("raised_by.user_id", ASCENDING), ("created_at", DESCENDING)])
    await db.alerts.create_index([("status", ASCENDING), ("location", "2dsphere")], sparse=True)

    # tasks
    await db.tasks.create_index([("assigned_to", ASCENDING), ("status", ASCENDING)])

    # drill sessions
    await db.drill_sessions.create_index([("employee_id", ASCENDING), ("completed_at", DESCENDING)])

    # safety checks
    await db.safety_checks.create_index([("employee_id", ASCENDING), ("generated_at", DESCENDING)])

    # refresh tokens (TTL — auto-expire after 7 days)
    await db.refresh_tokens.create_index(
        [("created_at", ASCENDING)],
        expireAfterSeconds=60 * 60 * 24 * 7,
    )
