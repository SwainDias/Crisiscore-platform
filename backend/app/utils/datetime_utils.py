"""
app/utils/datetime_utils.py
Centralised datetime helpers used across services.
"""

from datetime import UTC, datetime


def utcnow() -> datetime:
    """Returns the current UTC datetime (timezone-aware)."""
    return datetime.now(UTC)


def to_iso(dt: datetime | None) -> str:
    """Converts a datetime to ISO 8601 string. Falls back to now if None."""
    if dt is None:
        return utcnow().isoformat()
    return dt.isoformat()


def from_iso(value: str) -> datetime:
    """Parses an ISO 8601 string into a timezone-aware datetime."""
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return dt
