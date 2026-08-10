"""CP4 — Stateless conversation history stored in Redis."""

from __future__ import annotations

import json

import redis

from .config import get_settings

HISTORY_MAX_MESSAGES = 20
HISTORY_TTL_SECONDS = 7 * 24 * 3600


def get_redis_client(url: str | None = None):
    """Tạo Redis client; fake:// dùng fakeredis cho local/test."""
    resolved_url = url or get_settings().redis_url
    if resolved_url.startswith("fake://"):
        import fakeredis

        return fakeredis.FakeRedis(decode_responses=True)
    return redis.from_url(resolved_url, decode_responses=True)


class ConversationStore:
    """Lưu lịch sử hội thoại của từng user trong Redis List."""

    def __init__(self, client) -> None:
        self.client = client

    @staticmethod
    def _key(user_id: str) -> str:
        return f"history:{user_id}"

    def ping(self) -> bool:
        try:
            return bool(self.client.ping())
        except Exception:
            return False

    def append(self, user_id: str, role: str, content: str) -> None:
        key = self._key(user_id)
        message = json.dumps(
            {"role": role, "content": content},
            ensure_ascii=False,
        )
        self.client.rpush(key, message)
        self.client.ltrim(key, -HISTORY_MAX_MESSAGES, -1)
        self.client.expire(key, HISTORY_TTL_SECONDS)

    def get_history(self, user_id: str) -> list[dict]:
        values = self.client.lrange(self._key(user_id), 0, -1)
        return [json.loads(value) for value in values]

    def clear(self, user_id: str) -> None:
        self.client.delete(self._key(user_id))
