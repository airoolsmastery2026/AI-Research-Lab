"""Result objects for parsed documents."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class ParseStats:
    characters: int = 0
    words: int = 0
    tokens: int = 0
    paragraphs: int = 0
    headings: int = 0
    tables: int = 0
    images: int = 0
    pages: int = 0


@dataclass(slots=True)
class ParsedDocument:
    """Output container for parsed document content and metadata."""

    source_path: Path
    text: str
    language: str = "unknown"
    metadata: dict[str, Any] = field(default_factory=dict)
    stats: ParseStats = field(default_factory=ParseStats)
    pages: list[str] = field(default_factory=list)
    paragraphs: list[str] = field(default_factory=list)
    headings: list[str] = field(default_factory=list)
    tables: list[list[list[str]]] = field(default_factory=list)
    image_references: list[str] = field(default_factory=list)
