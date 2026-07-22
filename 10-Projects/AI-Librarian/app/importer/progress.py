"""Progress tracking helpers for the import pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ProgressStage(str, Enum):
    SCANNING = "scanning"
    FILTERING = "filtering"
    QUEUING = "queuing"
    IMPORTING = "importing"
    COMPLETE = "complete"
    FAILED = "failed"


@dataclass(slots=True)
class ImportProgress:
    """Tracks progress during import execution."""

    total_items: int = 0
    processed_items: int = 0
    failed_items: int = 0
    current_stage: ProgressStage = ProgressStage.SCANNING
    details: list[str] = field(default_factory=list)

    def mark_processed(self) -> None:
        self.processed_items += 1

    def mark_failed(self) -> None:
        self.failed_items += 1

    def update_stage(self, stage: ProgressStage) -> None:
        self.current_stage = stage

    def percent_complete(self) -> float:
        if not self.total_items:
            return 0.0
        return round((self.processed_items / self.total_items) * 100, 2)
