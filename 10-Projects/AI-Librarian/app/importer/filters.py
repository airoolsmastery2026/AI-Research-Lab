"""Filtering utilities for the import pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable


@dataclass(slots=True)
class ImportFilter:
    """Configurable filter for deciding whether a file should be imported."""

    name: str
    predicate: Callable[[Path], bool]
    enabled: bool = True


def build_default_filters() -> list[ImportFilter]:
    """Build the standard set of import filters."""

    def is_hidden(path: Path) -> bool:
        return any(part.startswith(".") for part in path.parts)

    def is_system(path: Path) -> bool:
        return path.name.lower().startswith("~") or path.name.lower().startswith("$")

    return [
        ImportFilter("hidden", is_hidden),
        ImportFilter("system", is_system),
    ]
