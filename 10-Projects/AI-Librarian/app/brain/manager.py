"""High-level brain manager for orchestrating AI Librarian subsystems."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .config import BrainConfig
from .events import BrainEvent
from .state import BrainState
from .tasks import BrainTask


class BrainManager:
    """Coordinate planning, execution, and state management."""

    def __init__(self, config: BrainConfig | None = None, state: BrainState | None = None) -> None:
        self.config = config or BrainConfig()
        self.state = state or BrainState()
        self._queue: list[BrainTask] = []

    def enqueue(self, task: BrainTask) -> None:
        self._queue.append(task)

    def process_pending(self) -> None:
        while self._queue:
            task = self._queue.pop(0)
            self._execute(task)

    def _execute(self, task: BrainTask) -> None:
        if task.kind == "import":
            self.state.tasks_completed += 1
            self.state.apply(BrainEvent(name="imported", payload={"task_id": task.task_id}))
        elif task.kind == "index":
            self.state.tasks_completed += 1
            self.state.apply(BrainEvent(name="indexed", payload={"task_id": task.task_id}))
        elif task.kind == "search":
            self.state.tasks_completed += 1
            self.state.apply(BrainEvent(name="searched", payload={"task_id": task.task_id}))
        else:
            self.state.tasks_completed += 1
            self.state.apply(BrainEvent(name="processed", payload={"task_id": task.task_id}))
