"""Conversation context helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .message import Message


@dataclass(slots=True)
class ConversationContext:
    messages: List[Message] = field(default_factory=list)

    def add_message(self, role: str, content: str) -> None:
        self.messages.append(Message(role=role, content=content))

    def to_prompt(self) -> str:
        return "\n".join(f"{message.role}: {message.content}" for message in self.messages)
