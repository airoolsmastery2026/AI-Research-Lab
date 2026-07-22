"""Orchestrator for coordinating subsystem operations."""

from __future__ import annotations

from .manager import BrainManager
from .tasks import BrainTask


class BrainOrchestrator:
    """Thin orchestrator for importing, indexing, and answering requests."""

    def __init__(self, manager: BrainManager | None = None) -> None:
        self.manager = manager or BrainManager()

    def import_documents(self, path: str) -> None:
        self.manager.enqueue(BrainTask(task_id="import", kind="import", payload={"path": path}))
        self.manager.process_pending()

    def build_knowledge_base(self, path: str) -> None:
        self.manager.enqueue(BrainTask(task_id="index", kind="index", payload={"path": path}))
        self.manager.process_pending()

    def search_knowledge(self, query: str) -> None:
        self.manager.enqueue(BrainTask(task_id="search", kind="search", payload={"query": query}))
        self.manager.process_pending()
