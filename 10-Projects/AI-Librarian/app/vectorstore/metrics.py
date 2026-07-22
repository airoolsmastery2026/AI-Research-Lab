"""Statistics for vector stores."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class VectorStoreMetrics:
    count: int = 0
    namespace: str = "default"
    backend: str = "memory"
