"""High-level manager for the RAG subsystem."""

from __future__ import annotations

from .answer_generator import AnswerGenerator, AnswerRequest, AnswerResponse
from .memory import ConversationMemory
from .history import ConversationHistory


class RAGManager:
    """Coordinate answer generation and session memory."""

    def __init__(self, answer_generator: AnswerGenerator | None = None, memory: ConversationMemory | None = None, history: ConversationHistory | None = None) -> None:
        self.answer_generator = answer_generator or AnswerGenerator()
        self.memory = memory or ConversationMemory()
        self.history = history or ConversationHistory()

    def answer(self, request: AnswerRequest) -> AnswerResponse:
        response = self.answer_generator.generate(request)
        self.memory.add("assistant", response.answer)
        self.history.add("user", request.question)
        self.history.add("assistant", response.answer)
        return response
