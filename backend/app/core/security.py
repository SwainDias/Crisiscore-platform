"""
app/core/security.py
JWT creation / verification and password hashing helpers.
Uses argon2-cffi for password hashing (replaces passlib/bcrypt).
"""

from datetime import UTC, datetime, timedelta
from typing import Any

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHashError
from jose import JWTError, jwt

from app.core.config import get_settings
from app.core.constants import AuthErrorCode
from app.core.exceptions import UnauthorizedException

settings = get_settings()

# Argon2id — RFC 9106 recommended defaults
_ph = PasswordHasher(
    time_cost=2,
    memory_cost=65536,  # 64 MB
    parallelism=2,
    hash_len=32,
    salt_len=16,
)


# ─── Password ────────────────────────────────────────────────────────────────

def hash_password(plain: str) -> str:
    """Return an Argon2id hash of *plain*."""
    return _ph.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    """
    Returns True if *plain* matches *hashed*.
    Argon2 raises on mismatch rather than returning False, so we normalise.
    """
    try:
        return _ph.verify(hashed, plain)
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return False


def needs_rehash(hashed: str) -> bool:
    """True if the stored hash was produced with outdated parameters."""
    return _ph.check_needs_rehash(hashed)


# ─── JWT ─────────────────────────────────────────────────────────────────────

def _create_token(data: dict[str, Any], expires_delta: timedelta) -> str:
    payload = data.copy()
    payload["exp"] = datetime.now(UTC) + expires_delta
    payload["iat"] = datetime.now(UTC)
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def create_access_token(subject: str, extra: dict[str, Any] | None = None) -> tuple[str, int]:
    """Returns (token, expires_in_seconds)."""
    delta = timedelta(minutes=settings.jwt_access_token_expire_minutes)
    data: dict[str, Any] = {"sub": subject, "type": "access"}
    if extra:
        data.update(extra)
    return _create_token(data, delta), int(delta.total_seconds())


def create_refresh_token(subject: str) -> str:
    delta = timedelta(days=settings.jwt_refresh_token_expire_days)
    return _create_token({"sub": subject, "type": "refresh"}, delta)


def decode_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
        )
    except JWTError as exc:
        raise UnauthorizedException(
            code=AuthErrorCode.TOKEN_INVALID, message="Token is invalid or expired."
        ) from exc