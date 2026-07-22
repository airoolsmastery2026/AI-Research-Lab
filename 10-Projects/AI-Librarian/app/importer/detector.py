"""File type detection for the import pipeline."""

from __future__ import annotations

import mimetypes
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".doc",
    ".txt",
    ".md",
    ".csv",
    ".xlsx",
    ".xls",
    ".pptx",
    ".ppt",
    ".epub",
    ".html",
    ".json",
    ".xml",
}


@dataclass(slots=True)
class FileTypeInfo:
    extension: str
    mime_type: str
    is_supported: bool


def detect_file_type(path: Path | str) -> FileTypeInfo:
    """Detect the file type for the supplied path."""

    candidate = Path(path).expanduser()
    extension = candidate.suffix.lower()
    guessed_type, _ = mimetypes.guess_type(candidate.name)
    mime_type = guessed_type or "application/octet-stream"
    return FileTypeInfo(
        extension=extension,
        mime_type=mime_type,
        is_supported=extension in SUPPORTED_EXTENSIONS,
    )


def supported_extensions() -> tuple[str, ...]:
    return tuple(sorted(SUPPORTED_EXTENSIONS))
