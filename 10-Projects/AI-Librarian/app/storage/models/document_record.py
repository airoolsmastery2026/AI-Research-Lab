"""Document record model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class DocumentRecord:
    id: str
    document_id: str
    title: str | None = None
    file_path: str = ""
    extension: str | None = None
    mime_type: str | None = None
    size_bytes: int | None = None
    sha256: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
