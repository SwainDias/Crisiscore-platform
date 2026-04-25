"""
app/core/config.py
Central application configuration loaded from environment variables.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Application ──────────────────────────────────────────────────────────
    app_env: str = "development"
    app_version: str = "1.0.0"
    debug: bool = False

    # ── MongoDB ──────────────────────────────────────────────────────────────
    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db_name: str = "rapid_response"

    # ── Redis ────────────────────────────────────────────────────────────────
    redis_url: str = "redis://localhost:6379/0"

    # ── JWT ──────────────────────────────────────────────────────────────────
    jwt_secret_key: str = "CHANGE_ME"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60
    jwt_refresh_token_expire_days: int = 7

    # ── Security ─────────────────────────────────────────────────────────────
    allowed_origins: str = "http://localhost:3000"
    max_login_attempts: int = 5
    account_lock_duration_minutes: int = 15

    # ── Feature Flags ─────────────────────────────────────────────────────────
    feature_biometrics_enabled: bool = True
    feature_micro_drill_enabled: bool = True
    feature_live_map_enabled: bool = True

    # ── Reports ───────────────────────────────────────────────────────────────
    report_export_base_url: str = "https://cdn.example.com/reports"
    report_export_expiry_hours: int = 24

    @property
    def allowed_origins_list(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",")]

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Cached singleton — import and call this everywhere."""
    return Settings()
