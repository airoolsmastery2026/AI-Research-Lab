"""Indexing helpers for vector stores."""

from __future__ import annotations

from typing import Iterable

from .base import VectorRecord


class VectorIndex:
    """Simple incremental index wrapper."""

    def __init__(self) -> None:
        self._records: list[VectorRecord] = []

    def add(self, record: VectorRecord) -> None:
        self._records.append(record)

    def add_many(self, records: Iterable[VectorRecord]) -> None:
        self._records.extend(records)

    def clear(self) -> None:
        self._records.clear()

    def count(self) -> int:
        return len(self._records)
