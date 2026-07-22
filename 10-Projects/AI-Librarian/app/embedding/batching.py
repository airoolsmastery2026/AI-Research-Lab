"""Batch processing helpers for embeddings."""

from __future__ import annotations

from collections import deque
from typing import TypeVar

T = TypeVar("T")


class BatchProcessor:
    """Split a list into batches of a target size."""

    def __init__(self, batch_size: int = 16) -> None:
        self.batch_size = batch_size

    def batch(self, items: list[T]) -> list[list[T]]:
        if not items:
            return []
        return [items[index : index + self.batch_size] for index in range(0, len(items), self.batch_size)]
