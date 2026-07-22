"""Knowledge base coordination helpers."""

from __future__ import annotations

from typing import Any


class KnowledgeManager:
    """Simple knowledge manager for storing and retrieving information."""

    def __init__(self) -> None:
        self._items: dict[str, Any] = {}

    def add(self, key: str, value: Any) -> None:
        self._items[key] = value

    def get(self, key: str) -> Any:
        return self._items.get(key)

    def search(self, query: str) -> list[Any]:
        return [value for key, value in self._items.items() if query.lower() in str(key).lower()]
