"""Typed data models for the embedding engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass(slots=True)
class Chunk:
    text: str
    start: int = 0
    end: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ChunkingConfig:
    chunk_size: int = 256
    overlap: int = 0
    strategy: str = "sentence"
    separators: tuple[str, ...] = ("\n\n", "\n", " ", "")


@dataclass(slots=True)
class EmbeddingRequest:
    texts: list[str]
    metadata: dict[str, Any] | None = None
    model: str | None = None


@dataclass(slots=True)
class EmbeddingResult:
    text: str
    embedding: list[float]
    metadata: dict[str, Any] = field(default_factory=dict)
