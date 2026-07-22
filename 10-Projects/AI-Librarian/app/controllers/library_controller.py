from __future__ import annotations

from app.brain import BrainManager


class LibraryController:
    def __init__(self, brain: BrainManager | None = None) -> None:
        self.brain = brain or BrainManager()

    def scan_documents(self) -> list[str]:
        return ["documents"]
