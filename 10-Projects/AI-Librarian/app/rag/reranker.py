"""Simple reranking utilities."""

from __future__ import annotations

from .retriever import RetrievalResult


class Reranker:
    """Reorder retrieval results by descending score."""

    def rerank(self, results: list[RetrievalResult]) -> list[RetrievalResult]:
        return sorted(results, key=lambda item: item.score, reverse=True)
