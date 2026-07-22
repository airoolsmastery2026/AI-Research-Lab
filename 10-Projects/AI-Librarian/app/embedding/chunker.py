"""Chunking orchestration with multiple strategies."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from .models import Chunk, ChunkingConfig
from .splitter import CodeTextSplitter, MarkdownTextSplitter, RecursiveTextSplitter


@dataclass(slots=True)
class ChunkStrategy:
    name: str
    splitter: Any


class Chunker:
    """Create text chunks using configured strategy."""

    def __init__(self, config: ChunkingConfig | None = None) -> None:
        self.config = config or ChunkingConfig()
        self._strategies = {
            "sentence": ChunkStrategy("sentence", RecursiveTextSplitter(chunk_size=self.config.chunk_size, overlap=self.config.overlap)),
            "recursive": ChunkStrategy("recursive", RecursiveTextSplitter(chunk_size=self.config.chunk_size, overlap=self.config.overlap)),
            "markdown": ChunkStrategy("markdown", MarkdownTextSplitter(chunk_size=self.config.chunk_size, overlap=self.config.overlap)),
            "code": ChunkStrategy("code", CodeTextSplitter(chunk_size=self.config.chunk_size, overlap=self.config.overlap)),
        }

    def chunk(self, text: str, config: ChunkingConfig | None = None) -> list[Chunk]:
        active = config or self.config
        strategy_name = active.strategy.lower()
        strategy = self._strategies.get(strategy_name)

        if strategy is None:
            strategy = self._strategies["sentence"]

        chunks = strategy.splitter.split(text)
        return self._apply_metadata(chunks, active)

    def _apply_metadata(self, chunks: list[Chunk], config: ChunkingConfig) -> list[Chunk]:
        for index, chunk in enumerate(chunks):
            chunk.metadata["strategy"] = config.strategy
            chunk.metadata["chunk_size"] = config.chunk_size
            chunk.metadata["overlap"] = config.overlap
            chunk.metadata["index"] = index
            chunk.start = index
            chunk.end = index + len(chunk.text)
        return chunks
