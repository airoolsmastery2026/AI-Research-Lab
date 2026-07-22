"""Conversation history utilities."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ConversationHistory:
    entries: list[dict[str, Any]] = field(default_factory=list)

    def add(self, role: str, content: str) -> None:
        self.entries.append({"role": role, "content": content})

    def compress(self, max_items: int = 4) -> list[dict[str, Any]]:
        return self.entries[-max_items:] if self.entries else []
