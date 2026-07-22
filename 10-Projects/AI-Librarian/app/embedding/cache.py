"""Simple embedding cache."""

from __future__ import annotations

from typing import Any


class EmbeddingCache:
    """In-memory cache keyed by normalized text."""

    def __init__(self) -> None:
        self._store: dict[str, Any] = {}

    def get(self, text: str) -> Any | None:
        return self._store.get(text.lower())

    def set(self, text: str, value: Any) -> None:
        self._store[text.lower()] = value

    def clear(self) -> None:
        self._store.clear()
