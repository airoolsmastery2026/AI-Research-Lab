"""Binary serializer helpers for storage layer values."""

from __future__ import annotations

import pickle
from typing import Any


class BinarySerializer:
    """Serialize values to bytes for binary storage."""

    @staticmethod
    def dumps(value: Any) -> bytes:
        return pickle.dumps(value)

    @staticmethod
    def loads(value: bytes) -> Any:
        return pickle.loads(value)
