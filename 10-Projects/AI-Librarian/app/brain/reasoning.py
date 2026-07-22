"""Reasoning helpers for planning and answering."""

from __future__ import annotations

from typing import Any


class Reasoner:
    """Provide simple heuristic reasoning over tasks and context."""

    def infer(self, task: str) -> str:
        return task.lower().replace(" ", "_")
