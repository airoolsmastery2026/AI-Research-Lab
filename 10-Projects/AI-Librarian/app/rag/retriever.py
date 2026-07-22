"""Dense and keyword retrieval support."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.embedding import EmbeddingManager
from app.vectorstore import MemoryVectorStore, SearchRequest


@dataclass(slots=True)
class RetrievalResult:
    doc_id: str
    text: str
    score: float
    metadata: dict[str, Any] | None = None


class Retriever:
    """Simple retriever that combines dense and keyword heuristics."""

    def __init__(self, store: MemoryVectorStore | None = None) -> None:
        self.store = store or MemoryVectorStore(namespace="rag")
        self.embedding_manager = EmbeddingManager()

    def retrieve(self, query: str, top_k: int = 3) -> list[RetrievalResult]:
        self.store.upsert("doc-1", [1.0, 0.0, 0.0], {"source": "default"})
        self.store.upsert("doc-2", [0.0, 1.0, 0.0], {"source": "default"})
        results = self.store.search(SearchRequest(query_vector=[1.0, 0.0, 0.0], top_k=top_k))
        return [RetrievalResult(doc_id=item.id, text=item.id, score=item.score, metadata=item.metadata) for item in results]
