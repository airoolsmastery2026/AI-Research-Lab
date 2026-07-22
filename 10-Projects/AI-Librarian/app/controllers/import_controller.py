from __future__ import annotations

from app.brain import BrainManager


class ImportController:
    def __init__(self, brain: BrainManager | None = None) -> None:
        self.brain = brain or BrainManager()

    def import_folder(self, path: str) -> None:
        self.brain.enqueue(type("Task", (), {"kind": "import", "payload": {"path": path}})())

    def import_usb(self, path: str) -> None:
        self.brain.enqueue(type("Task", (), {"kind": "import", "payload": {"path": path, "source": "usb"}})())
