"""Simple evaluation metrics for RAG outputs."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class EvaluationResult:
    score: float = 0.0
    latency_ms: float = 0.0
    retrieved_count: int = 0
