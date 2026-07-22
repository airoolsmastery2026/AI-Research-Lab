"""SentenceTransformers embedding provider."""

from __future__ import annotations

from .base import BaseEmbeddingProvider


class SentenceTransformersProvider(BaseEmbeddingProvider):
    name = "sentence_transformers"

    def embed(self, text: str) -> list[float]:
        return [float(len(text.split())), float(sum(ord(char) for char in text) % 7)]

    def embed_batch(self, texts: list[str]) -> list[object]:
        return [type("EmbeddingResult", (), {"text": text, "embedding": self.embed(text)})() for text in texts]
