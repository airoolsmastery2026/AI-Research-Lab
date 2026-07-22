"""Query rewriting helpers for better retrieval."""

from __future__ import annotations


class QueryRewriter:
    """Rewrite user queries into a more retrieval-friendly form."""

    def rewrite(self, query: str) -> str:
        cleaned = query.strip()
        if not cleaned:
            return ""
        return f"{cleaned} context"
