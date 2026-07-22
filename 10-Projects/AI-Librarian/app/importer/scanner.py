"""Recursive document scanning for the import pipeline."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Sequence

from app.core.logger import get_logger
from app.metadata import extract_metadata

from .detector import detect_file_type
from .filters import ImportFilter

logger = get_logger("importer.scanner")


def scan_documents(
    root_dir: Path | str,
    *,
    filters: Sequence[ImportFilter] | None = None,
    recursive: bool = True,
) -> list[Path]:
    """Scan a directory for files that should be imported."""

    root = Path(root_dir).expanduser().resolve()
    if not root.exists():
        return []

    discovered: list[Path] = []
    for path in root.rglob("*") if recursive else root.glob("*"):
        if not path.is_file():
            continue
        if _should_skip(path, filters):
            continue
        file_type = detect_file_type(path)
        if not file_type.is_supported:
            continue
        discovered.append(path)
    return sorted(discovered)


def _should_skip(path: Path, filters: Sequence[ImportFilter] | None) -> bool:
    if filters is None:
        return False
    for filter_item in filters:
        if filter_item.enabled and filter_item.predicate(path):
            return True
    return False
