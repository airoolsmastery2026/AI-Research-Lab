"""Search request and result models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .filters import FilterCriteria


@dataclass(slots=True)
class SearchRequest:
    query_vector: list[float]
    top_k: int = 5
    filters: FilterCriteria | None = None


@dataclass(slots=True)
class SearchResult:
    id: str
    score: float
    metadata: dict[str, Any] = field(default_factory=dict)
