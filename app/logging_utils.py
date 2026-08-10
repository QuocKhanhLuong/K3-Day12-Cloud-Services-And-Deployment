"""CP1 — Structured logging."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone


def utc_now_iso() -> str:
    """Thời điểm hiện tại theo ISO-8601, múi giờ UTC."""
    return datetime.now(timezone.utc).isoformat()


def log_event(event: str, level: str = "info", **fields) -> str:
    """Ghi một JSON object trên đúng một dòng ra stdout và trả về chuỗi đó."""
    payload = {
        "event": event,
        "level": level.lower(),
        "timestamp": utc_now_iso(),
        **fields,
    }
    raw = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    print(raw, file=sys.stdout, flush=True)
    return raw
