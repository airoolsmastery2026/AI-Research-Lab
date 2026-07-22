from __future__ import annotations

from pathlib import Path
from typing import Any

from app.brain import BrainManager
from ._compat import ensure_qapplication
from .signals import Signal


class LibraryPanel:
    def __init__(self, brain: BrainManager | None = None) -> None:
        ensure_qapplication()
        self.brain = brain or BrainManager()
        self.items: list[dict[str, Any]] = []
        self.items_changed = Signal()

    def refresh(self, path: str) -> list[dict[str, Any]]:
        root = Path(path)
        self.items = [
            {"name": child.name, "path": str(child), "is_dir": child.is_dir()} for child in sorted(root.iterdir())
        ]
        self.brain.enqueue(type("BrainTask", (), {"kind": "import", "payload": {"path": path}})())
        self.items_changed.emit(self.items)
        return self.items
