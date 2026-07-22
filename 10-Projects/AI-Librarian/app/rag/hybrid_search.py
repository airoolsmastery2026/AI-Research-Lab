"""Hybrid search combining dense and keyword signals."""

from __future__ import annotations

from .retriever import RetrievalResult, Retriever


class HybridSearch:
    """Simple hybrid retrieval wrapper."""

    def __init__(self, retriever: Retriever | None = None) -> None:
        self.retriever = retriever or Retriever()

    def search(self, query: str, top_k: int = 3) -> list[RetrievalResult]:
        return self.retriever.retrieve(query, top_k=top_k)
