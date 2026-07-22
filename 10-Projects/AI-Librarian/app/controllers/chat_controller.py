from __future__ import annotations

from app.brain import BrainManager


class ChatController:
    def __init__(self, brain: BrainManager | None = None) -> None:
        self.brain = brain or BrainManager()

    def send_message(self, message: str) -> str:
        self.brain.enqueue(type("Task", (), {"kind": "chat", "payload": {"message": message}})())
        return f"Echo: {message}"
