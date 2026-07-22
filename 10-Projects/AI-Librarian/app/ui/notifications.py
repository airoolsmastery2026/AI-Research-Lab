from __future__ import annotations

from collections import deque

from ._compat import ensure_qapplication
from .signals import Signal


class NotificationCenter:
    def __init__(self) -> None:
        ensure_qapplication()
        self._messages: deque[tuple[str, str]] = deque()
        self.message_received = Signal()

    def notify(self, title: str, message: str) -> None:
        self._messages.append((title, message))
        self.message_received.emit(title, message)

    def unread_count(self) -> int:
        return len(self._messages)

    def pop(self) -> tuple[str, str] | None:
        if self._messages:
            return self._messages.popleft()
        return None
