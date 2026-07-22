"""Prompt template builder for RAG answers."""

from __future__ import annotations


class PromptBuilder:
    """Build a prompt from context and a question."""

    def build(self, question: str, context: str | None = None) -> str:
        base = f"Answer the following question using the provided context.\n\nQuestion: {question}\n"
        if context:
            return base + f"\nContext:\n{context}\n"
        return base
