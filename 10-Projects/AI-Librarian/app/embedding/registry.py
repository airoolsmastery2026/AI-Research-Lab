"""Registry for embedding providers."""

from __future__ import annotations

from typing import Dict, Type

from .providers.base import BaseEmbeddingProvider


class ProviderRegistry:
    """Simple registry for supported providers."""

    def __init__(self) -> None:
        self._providers: Dict[str, Type[BaseEmbeddingProvider]] = {}

    def register(self, name: str, provider_cls: Type[BaseEmbeddingProvider]) -> None:
        self._providers[name.lower()] = provider_cls

    def get(self, name: str) -> Type[BaseEmbeddingProvider] | None:
        return self._providers.get(name.lower())

    def list(self) -> list[str]:
        return sorted(self._providers)
