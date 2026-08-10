"""CP1 — Cấu hình theo 12-Factor.

Nguyên tắc: cấu hình đến từ biến môi trường để cùng một image chạy được ở
laptop, staging và production mà không phải sửa code.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Toàn bộ cấu hình của service."""

    port: int = 8000
    agent_api_key: str
    redis_url: str = "redis://localhost:6379/0"
    rate_limit_per_minute: int = 10
    monthly_budget_usd: float = 10.0
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("agent_api_key")
    @classmethod
    def validate_agent_api_key(cls, value: str) -> str:
        """Fail-fast khi secret rỗng hoặc vẫn là placeholder của starter repo."""
        cleaned = value.strip()
        placeholders = {
            "changeme",
            "change-me",
            "doi-thanh-khoa-cua-rieng-ban",
            "your-api-key",
        }
        if not cleaned or cleaned.lower() in placeholders:
            raise ValueError("AGENT_API_KEY must be set to a real non-placeholder value")
        return cleaned


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Đọc cấu hình một lần rồi cache lại."""
    return Settings()
