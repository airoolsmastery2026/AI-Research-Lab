"""Cache manager abstraction for storage layer caches."""

from __future__ import annotations

from typing import Any, Protocol


class CacheManager(Protocol):
    """Protocol describing basic cache operations."""

    def get(self, key: str) -> Any | None:
        ...

    def set(self, key: str, value: Any) -> None:
        ...

    def delete(self, key: str) -> None:
        ...
