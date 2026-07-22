"""Base abstraction for embedding providers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseEmbeddingProvider(ABC):
    """Interface for embedding providers."""

    name: str = "base"

    @abstractmethod
    def embed(self, text: str) -> list[float]:
        """Create an embedding for a single text."""

    def embed_batch(self, texts: list[str]) -> list[EmbeddingResult]:
        return [self.embed(text) for text in texts]
