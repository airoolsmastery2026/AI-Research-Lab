"""Gemini embedding provider."""

from __future__ import annotations

from .base import BaseEmbeddingProvider


class GeminiProvider(BaseEmbeddingProvider):
    name = "gemini"

    def embed(self, text: str) -> list[float]:
        return [float(len(text)), float(len(text.split()))]
