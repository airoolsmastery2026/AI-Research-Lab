"""Validation helpers for metadata extraction."""

from __future__ import annotations

import os
from pathlib import Path

from app.core.exceptions import ConfigurationError

from .models import ValidationReport


def validate_document_path(path: Path) -> ValidationReport:
    """Validate that a document path is usable and readable."""

    report = ValidationReport(is_valid=True)
    candidate = Path(path).expanduser()

    if not candidate.exists():
        report.add_issue("Path does not exist")
        return report

    if not candidate.is_file():
        report.add_issue("Path is not a regular file")
        return report

    try:
        with candidate.open("rb"):
            pass
    except OSError as exc:
        report.add_issue(f"Unable to read file: {exc}")

    return report
