"""Ollama embedding provider."""

from __future__ import annotations

from .base import BaseEmbeddingProvider


class OllamaProvider(BaseEmbeddingProvider):
    name = "ollama"

    def embed(self, text: str) -> list[float]:
        return [float(len(text)), float(sum(ord(char) for char in text) % 13)]
