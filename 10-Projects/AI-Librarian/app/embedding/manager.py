"""High-level embedding manager."""

from __future__ import annotations

from typing import Any, Iterable

from .batching import BatchProcessor
from .cache import EmbeddingCache
from .chunker import Chunker
from .models import Chunk, ChunkingConfig, EmbeddingRequest, EmbeddingResult
from .providers.base import BaseEmbeddingProvider
from .providers.openai import OpenAIProvider
from .tokenizer import count_tokens
from .normalizer import normalize_vector
from .similarity import cosine_similarity, dot_product


class EmbeddingManager:
    """Manage chunking, caching, batching, and embedding generation."""

    def __init__(self, provider: BaseEmbeddingProvider | None = None, cache: EmbeddingCache | None = None, batch_size: int = 16) -> None:
        self.provider = provider or OpenAIProvider()
        self.cache = cache or EmbeddingCache()
        self.batch_processor = BatchProcessor(batch_size=batch_size)
        self.chunker = Chunker()

    @staticmethod
    def chunk_text(text: str, config: ChunkingConfig | None = None) -> list[Chunk]:
        return Chunker(config or ChunkingConfig()).chunk(text, config)

    def embed(self, request: EmbeddingRequest) -> list[EmbeddingResult]:
        results: list[EmbeddingResult] = []
        for text in request.texts:
            cached = self.cache.get(text)
            if cached is not None:
                results.append(EmbeddingResult(text=text, embedding=list(cached), metadata=request.metadata or {}))
                continue

            embedding = self.provider.embed(text)
            self.cache.set(text, embedding)
            results.append(EmbeddingResult(text=text, embedding=embedding, metadata=request.metadata or {}))
        return results

    def embed_chunks(self, chunks: list[Chunk], metadata: dict[str, Any] | None = None) -> list[EmbeddingResult]:
        results: list[EmbeddingResult] = []
        for chunk in chunks:
            embedding = self.provider.embed(chunk.text)
            results.append(EmbeddingResult(text=chunk.text, embedding=embedding, metadata={**(metadata or {}), **chunk.metadata}))
        return results

    def deduplicate(self, texts: Iterable[str]) -> list[str]:
        seen: set[str] = set()
        deduped: list[str] = []
        for text in texts:
            if text in seen:
                continue
            seen.add(text)
            deduped.append(text)
        return deduped

    def stream_embeddings(self, texts: Iterable[str]) -> Iterable[EmbeddingResult]:
        for text in texts:
            yield EmbeddingResult(text=text, embedding=self.provider.embed(text), metadata={"stream": True})

    def count_tokens(self, text: str) -> int:
        return count_tokens(text)

    def normalize(self, vector: list[float]) -> list[float]:
        return normalize_vector(vector)

    def cosine_similarity(self, a: list[float], b: list[float]) -> float:
        return cosine_similarity(a, b)

    def dot_product(self, a: list[float], b: list[float]) -> float:
        return dot_product(a, b)
