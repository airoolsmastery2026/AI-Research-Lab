"""Search index manager for documents and chunks."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class SearchIndex:
    """In-memory search index registry for document identifiers."""

    entries: dict[str, list[str]] = field(default_factory=dict)

    def add(self, document_id: str, terms: list[str]) -> None:
        self.entries[document_id] = terms

    def remove(self, document_id: str) -> None:
        self.entries.pop(document_id, None)

    def search(self, term: str) -> list[str]:
        return [document_id for document_id, terms in self.entries.items() if term in terms]
