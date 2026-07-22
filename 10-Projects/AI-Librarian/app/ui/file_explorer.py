from __future__ import annotations

from pathlib import Path
from typing import Any

from app.brain import BrainManager
from ._compat import ensure_qapplication
from .signals import Signal


class FileExplorer:
    def __init__(self, brain: BrainManager | None = None) -> None:
        ensure_qapplication()
        self.brain = brain or BrainManager()
        self.root = None
        self.entries: list[dict[str, Any]] = []
        self.selection_changed = Signal()

    def load_directory(self, path: str) -> list[dict[str, Any]]:
        root = Path(path)
        self.root = root
        self.entries = [
            {"name": child.name, "path": str(child), "is_dir": child.is_dir()} for child in sorted(root.iterdir())
        ]
        self.brain.enqueue(type("BrainTask", (), {"kind": "index", "payload": {"path": path}})())
        self.selection_changed.emit(self.entries)
        return self.entries
