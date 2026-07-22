"""Base abstraction for vector stores."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from .errors import VectorStoreError
from .filters import FilterCriteria
from .search import SearchRequest, SearchResult


@dataclass(slots=True)
class VectorRecord:
    id: str
    vector: list[float]
    metadata: dict[str, Any] = field(default_factory=dict)


class BaseVectorStore(ABC):
    """Abstract repository interface for vector storage backends."""

    def __init__(self, namespace: str = "default") -> None:
        self.namespace = namespace

    @abstractmethod
    def upsert(self, record_id: str, vector: list[float], metadata: dict[str, Any] | None = None) -> None:
        """Insert or update a vector."""

    @abstractmethod
    def get(self, record_id: str) -> VectorRecord | None:
        """Return a vector record by id."""

    @abstractmethod
    def search(self, request: SearchRequest) -> list[SearchResult]:
        """Search the vector store."""

    @abstractmethod
    def delete(self, record_id: str) -> None:
        """Delete a record."""

    @abstractmethod
    def stats(self) -> dict[str, Any]:
        """Return store statistics."""
