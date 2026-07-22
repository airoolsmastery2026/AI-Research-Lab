"""Planning utilities for multi-step Brain workflows."""

from __future__ import annotations

from .tasks import BrainTask


class Planner:
    """Schedule a simple sequence of tasks."""

    def plan(self, goal: str) -> list[BrainTask]:
        return [
            BrainTask(task_id="plan-import", kind="import", payload={"goal": goal}),
            BrainTask(task_id="plan-index", kind="index", payload={"goal": goal}),
        ]
