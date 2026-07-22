"""Dispatching logic for import jobs."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Sequence

from app.core.logger import get_logger
from app.metadata import DocumentMetadata, extract_metadata

from .errors import ImportValidationError
from .queue import ImportQueue, ImportQueueItem

logger = get_logger("importer.dispatcher")


@dataclass(slots=True)
class ImportDispatcher:
    """Dispatches queued files into metadata extraction and validation."""

    queue: ImportQueue[ImportQueueItem] = field(default_factory=ImportQueue)

    def enqueue_path(self, path: Path) -> None:
        self.queue.enqueue(ImportQueueItem(path=path))

    def dispatch(self, *, batch_size: int = 10) -> list[DocumentMetadata]:
        processed: list[DocumentMetadata] = []
        while self.queue.size() and batch_size > 0:
            item = self.queue.dequeue()
            if item is None:
                continue
            metadata = self._build_metadata(item.path)
            item.metadata = metadata
            processed.append(metadata)
            batch_size -= 1
        return processed

    def _build_metadata(self, path: Path) -> DocumentMetadata:
        metadata = extract_metadata(path)
        if not metadata.validation_report.is_valid:
            raise ImportValidationError(f"Validation failed for {path}")
        return metadata
