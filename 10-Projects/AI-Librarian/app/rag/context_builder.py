"""Context construction and window management."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ContextDocument:
    doc_id: str
    text: str
    score: float
    metadata: dict[str, Any] = field(default_factory=dict)


class ContextBuilder:
    """Build a compact context window from retrieval results."""

    def build(self, documents: list[ContextDocument], max_items: int = 4) -> list[ContextDocument]:
        return documents[:max_items]
