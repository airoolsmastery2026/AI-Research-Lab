"""Conversation memory for RAG sessions."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ConversationMemory:
    entries: list[dict[str, Any]] = field(default_factory=list)

    def add(self, role: str, content: str) -> None:
        self.entries.append({"role": role, "content": content})

    def last(self) -> dict[str, Any] | None:
        return self.entries[-1] if self.entries else None
