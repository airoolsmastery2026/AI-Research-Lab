"""Workspace context for the Brain."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class Workspace:
    root: str = "."
    files: list[str] = field(default_factory=list)

    def scan(self) -> list[str]:
        root = Path(self.root)
        if not root.exists():
            return []
        return [str(path) for path in root.rglob("*") if path.is_file()]
