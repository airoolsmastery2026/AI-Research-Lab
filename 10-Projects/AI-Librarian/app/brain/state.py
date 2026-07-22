"""Persistent state for the Brain."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4

from .events import BrainEvent


@dataclass(slots=True)
class BrainState:
    session_id: str = field(default_factory=lambda: str(uuid4()))
    tasks_completed: int = 0
    last_event: BrainEvent | None = None

    def apply(self, event: BrainEvent) -> None:
        self.last_event = event
