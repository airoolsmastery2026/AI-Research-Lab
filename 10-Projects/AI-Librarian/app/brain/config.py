"""Configuration for the Brain subsystem."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class BrainConfig:
    namespace: str = "ai-librarian"
    enable_background_indexing: bool = True
    enable_event_bus: bool = True
    enable_persistence: bool = True
