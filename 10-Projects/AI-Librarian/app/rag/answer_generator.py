"""Answer generation for the RAG pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .citation import Citation
from .context_builder import ContextDocument
from .pipeline import RAGPipeline


@dataclass(slots=True)
class AnswerRequest:
    question: str
    top_k: int = 3


@dataclass(slots=True)
class AnswerResponse:
    answer: str
    context_documents: list[ContextDocument] = field(default_factory=list)
    citations: list[Citation] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class AnswerGenerator:
    """Generate a RAG answer from the pipeline output."""

    def __init__(self, pipeline: RAGPipeline | None = None) -> None:
        self.pipeline = pipeline or RAGPipeline()

    def generate(self, request: AnswerRequest) -> AnswerResponse:
        context_documents, prompt, citations = self.pipeline.run(request.question, top_k=request.top_k)
        answer = f"Answer based on: {prompt[:80]}"
        return AnswerResponse(answer=answer, context_documents=context_documents, citations=citations, metadata={"prompt": prompt})
