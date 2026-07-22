"""Text splitters for embedding chunking."""

from __future__ import annotations

import re
from typing import List

from .models import Chunk


class RecursiveTextSplitter:
    """Split text recursively by separators."""

    def __init__(self, chunk_size: int = 256, overlap: int = 0) -> None:
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split(self, text: str, metadata: dict | None = None) -> list[Chunk]:
        pieces = re.split(r"\n{2,}|\n|\s+", text.strip())
        pieces = [piece for piece in pieces if piece]
        chunks: list[Chunk] = []
        current: list[str] = []
        current_length = 0

        for piece in pieces:
            if current and current_length + len(piece.split()) > self.chunk_size:
                chunks.append(Chunk(text=" ".join(current), metadata=metadata or {}))
                current = []
                current_length = 0
            current.append(piece)
            current_length += len(piece.split())

        if current:
            chunks.append(Chunk(text=" ".join(current), metadata=metadata or {}))

        if self.overlap and len(chunks) > 1:
            return self._apply_overlap(chunks)
        return chunks

    def _apply_overlap(self, chunks: list[Chunk]) -> list[Chunk]:
        overlapped: list[Chunk] = []
        for index, chunk in enumerate(chunks):
            if index == 0:
                overlapped.append(chunk)
                continue
            previous = chunks[index - 1]
            merged = f"{previous.text} {chunk.text}"
            overlapped.append(Chunk(text=merged, metadata=chunk.metadata))
        return overlapped


class MarkdownTextSplitter:
    """Split markdown text into sections."""

    def __init__(self, chunk_size: int = 256, overlap: int = 0) -> None:
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split(self, text: str, metadata: dict | None = None) -> list[Chunk]:
        blocks = re.split(r"\n(?=#)", text)
        chunks: list[Chunk] = []
        for block in blocks:
            block = block.strip()
            if not block:
                continue
            chunks.append(Chunk(text=block, metadata=metadata or {}))
        return chunks[:3] if chunks else []


class CodeTextSplitter:
    """Split code blocks into smaller chunks."""

    def __init__(self, chunk_size: int = 256, overlap: int = 0) -> None:
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split(self, text: str, metadata: dict | None = None) -> list[Chunk]:
        lines = text.splitlines()
        chunks: list[Chunk] = []
        current: list[str] = []
        for line in lines:
            current.append(line)
            if len("\n".join(current)) > self.chunk_size:
                chunks.append(Chunk(text="\n".join(current), metadata=metadata or {}))
                current = []
        if current:
            chunks.append(Chunk(text="\n".join(current), metadata=metadata or {}))
        return chunks
