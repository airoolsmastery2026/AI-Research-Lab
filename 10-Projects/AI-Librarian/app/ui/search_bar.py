from __future__ import annotations

from app.brain import BrainManager
from ._compat import ensure_qapplication
from .signals import Signal


class SearchBar:
    def __init__(self, brain: BrainManager | None = None) -> None:
        ensure_qapplication()
        self.brain = brain or BrainManager()
        self.query = ""
        self.results: list[str] = []
        self.search_completed = Signal()

    def search(self, query: str) -> list[str]:
        self.query = query
        self.results = [query]
        self.brain.enqueue(type("BrainTask", (), {"kind": "search", "payload": {"query": query}})())
        self.search_completed.emit(self.results)
        return self.results
