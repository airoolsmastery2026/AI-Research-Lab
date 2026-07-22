from __future__ import annotations

from typing import Any, Callable


class Signal:
    def __init__(self) -> None:
        self._slots: list[Callable[..., Any]] = []

    def connect(self, slot: Callable[..., Any]) -> Callable[..., Any]:
        self._slots.append(slot)
        return slot

    def emit(self, *args: Any, **kwargs: Any) -> None:
        for slot in list(self._slots):
            slot(*args, **kwargs)
