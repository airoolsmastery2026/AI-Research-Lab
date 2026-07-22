"""Queue management for import jobs."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Generic, TypeVar

from app.metadata import DocumentMetadata, extract_metadata

T = TypeVar("T")


@dataclass(slots=True)
class ImportQueueItem:
    """Represents one queued import task."""

    path: Path
    metadata: DocumentMetadata | None = None


@dataclass(slots=True)
class ImportQueue(Generic[T]):
    """Simple FIFO queue for import jobs."""

    items: list[T] = field(default_factory=list)

    def enqueue(self, item: T) -> None:
        self.items.append(item)

    def dequeue(self) -> T | None:
        if not self.items:
            return None
        return self.items.pop(0)

    def size(self) -> int:
        return len(self.items)

    def clear(self) -> None:
        self.items.clear()

    def to_list(self) -> list[T]:
        return list(self.items)
