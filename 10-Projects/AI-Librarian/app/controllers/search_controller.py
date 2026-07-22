from __future__ import annotations

from app.brain import BrainManager


class SearchController:
    def __init__(self, brain: BrainManager | None = None) -> None:
        self.brain = brain or BrainManager()

    def search(self, query: str) -> list[str]:
        self.brain.enqueue(type("Task", (), {"kind": "search", "payload": {"query": query}})())
        return [query]
