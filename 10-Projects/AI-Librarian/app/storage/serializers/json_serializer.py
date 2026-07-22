"""JSON serializer helpers for storage layer records."""

from __future__ import annotations

import json
from typing import Any


class JsonSerializer:
    """Serialize and deserialize JSON-compatible values."""

    @staticmethod
    def dumps(value: Any) -> str:
        return json.dumps(value, ensure_ascii=False, sort_keys=True)

    @staticmethod
    def loads(value: str) -> Any:
        return json.loads(value)
