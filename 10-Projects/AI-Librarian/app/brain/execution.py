"""Execution helpers for queued tasks."""

from __future__ import annotations

from .manager import BrainManager
from .tasks import BrainTask


class TaskExecutor:
    """Execute queued tasks against a brain manager."""

    def __init__(self, manager: BrainManager | None = None) -> None:
        self.manager = manager or BrainManager()

    def execute(self, tasks: list[BrainTask]) -> None:
        for task in tasks:
            self.manager.enqueue(task)
        self.manager.process_pending()
