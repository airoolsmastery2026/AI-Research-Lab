from __future__ import annotations

from app.brain import BrainManager
from ._compat import ensure_qapplication
from .signals import Signal


class StartupWizard:
    def __init__(self, brain: BrainManager | None = None) -> None:
        ensure_qapplication()
        self.brain = brain or BrainManager()
        self.completed = False
        self.completed_signal = Signal()

    def run(self) -> None:
        self.completed = True
        self.brain.enqueue(type("BrainTask", (), {"kind": "index", "payload": {"step": "startup"}})())
        self.completed_signal.emit(self.completed)
