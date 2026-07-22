from __future__ import annotations

from pathlib import Path
from typing import Any

from app.brain import BrainManager
from ._compat import ensure_qapplication
from .signals import Signal


class DocumentViewer:
    def __init__(self, brain: BrainManager | None = None) -> None:
        ensure_qapplication()
        self.brain = brain or BrainManager()
        self.document: str | None = None
        self.content: str = ""
        self.metadata: dict[str, Any] = {}
        self.document_changed = Signal()

    def show_document(self, path: str) -> dict[str, Any]:
        target = Path(path)
        self.document = str(target)
        self.content = target.read_text(encoding="utf-8", errors="ignore") if target.exists() else ""
        self.metadata = {"path": str(target), "exists": target.exists()}
        self.brain.enqueue(type("BrainTask", (), {"kind": "search", "payload": {"query": str(target)}})())
        self.document_changed.emit(self.metadata)
        return self.metadata
