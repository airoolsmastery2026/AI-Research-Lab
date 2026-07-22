"""Embedding record model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class EmbeddingRecord:
    id: str
    document_id: str
    vector: list[float]
    metadata: dict[str, Any] = field(default_factory=dict)
