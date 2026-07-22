"""Task model for Brain workflows."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class BrainTask:
    task_id: str
    kind: str
    payload: dict[str, Any] = field(default_factory=dict)
