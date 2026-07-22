from __future__ import annotations

from app.brain import BrainManager
from ._compat import ensure_qapplication
from .signals import Signal


class OCRProgressWindow:
    def __init__(self, brain: BrainManager | None = None) -> None:
        ensure_qapplication()
        self.brain = brain or BrainManager()
        self.progress = 0

    def start(self) -> None:
        self.progress = 10
        self.brain.enqueue(type("BrainTask", (), {"kind": "index", "payload": {"step": "ocr"}})())
        self.completed.emit(self.progress)


class BackgroundIndexProgress:
    def __init__(self, brain: BrainManager | None = None) -> None:
        ensure_qapplication()
        self.brain = brain or BrainManager()
        self.progress = 0

    def start(self) -> None:
        self.progress = 25
        self.brain.enqueue(type("BrainTask", (), {"kind": "index", "payload": {"step": "background"}})())
        self.completed.emit(self.progress)
