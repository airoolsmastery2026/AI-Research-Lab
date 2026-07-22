"""Core RAG pipeline orchestration."""

from __future__ import annotations

from .context_builder import ContextBuilder, ContextDocument
from .retriever import Retriever
from .reranker import Reranker
from .prompt_builder import PromptBuilder
from .query_rewriter import QueryRewriter
from .citation import Citation


class RAGPipeline:
    """Coordinate retrieval, reranking, context building, and prompt creation."""

    def __init__(self, retriever: Retriever | None = None, reranker: Reranker | None = None, context_builder: ContextBuilder | None = None, prompt_builder: PromptBuilder | None = None, query_rewriter: QueryRewriter | None = None) -> None:
        self.retriever = retriever or Retriever()
        self.reranker = reranker or Reranker()
        self.context_builder = context_builder or ContextBuilder()
        self.prompt_builder = prompt_builder or PromptBuilder()
        self.query_rewriter = query_rewriter or QueryRewriter()

    def run(self, question: str, top_k: int = 3) -> tuple[list[ContextDocument], str, list[Citation]]:
        rewritten = self.query_rewriter.rewrite(question)
        results = self.retriever.retrieve(rewritten, top_k=top_k)
        ranked = self.reranker.rerank(results)
        context_documents = [ContextDocument(doc_id=item.doc_id, text=item.text, score=item.score, metadata=item.metadata or {}) for item in ranked]
        context = self.context_builder.build(context_documents)
        prompt = self.prompt_builder.build(question, "\n".join(item.text for item in context))
        citations = [Citation(source=item.doc_id) for item in context]
        return context, prompt, citations
