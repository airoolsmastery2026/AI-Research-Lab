from __future__ import annotations

from app.brain import BrainManager
from ._compat import ensure_qapplication
from .signals import Signal


class ImportFolderWizard:
    def __init__(self, brain: BrainManager | None = None) -> None:
        ensure_qapplication()
        self.brain = brain or BrainManager()
        self.path = ""

    def run(self, path: str) -> None:
        self.path = path
        self.brain.enqueue(type("BrainTask", (), {"kind": "import", "payload": {"path": path, "source": "folder"}})())
        self.imported.emit(path)


class ImportUSBWizard:
    def __init__(self, brain: BrainManager | None = None) -> None:
        ensure_qapplication()
        self.brain = brain or BrainManager()
        self.path = ""

    def run(self, path: str) -> None:
        self.path = path
        self.brain.enqueue(type("BrainTask", (), {"kind": "import", "payload": {"path": path, "source": "usb"}})())
        self.imported.emit(path)
