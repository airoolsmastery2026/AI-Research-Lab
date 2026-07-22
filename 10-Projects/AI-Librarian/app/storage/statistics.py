"""Storage statistics helpers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class StorageStatistics:
    document_count: int = 0
    chunk_count: int = 0
    embedding_count: int = 0
    history_count: int = 0
    cache_entries: int = 0
