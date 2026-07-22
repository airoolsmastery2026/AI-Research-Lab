"""Simple streaming response container."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class StreamingResponse:
    chunks: list[str] = field(default_factory=list)
