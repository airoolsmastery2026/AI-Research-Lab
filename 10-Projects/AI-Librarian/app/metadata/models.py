"""Core dataclasses used by the metadata engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class ValidationReport:
    """Represents the outcome of metadata validation."""

    is_valid: bool
    issues: list[str] = field(default_factory=list)

    def add_issue(self, issue: str) -> None:
        self.issues.append(issue)
        self.is_valid = False


@dataclass(slots=True)
class DocumentMetadata:
    """Structured metadata for a single document."""

    file_name: str
    absolute_path: Path
    relative_path: str
    extension: str
    mime_type: str
    file_size_bytes: int
    sha256: str
    created_time: datetime | None
    modified_time: datetime | None
    accessed_time: datetime | None
    file_owner: str | None
    language: str
    document_id: str
    validation_report: ValidationReport
    source_hash: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "file_name": self.file_name,
            "absolute_path": str(self.absolute_path),
            "relative_path": self.relative_path,
            "extension": self.extension,
            "mime_type": self.mime_type,
            "file_size_bytes": self.file_size_bytes,
            "sha256": self.sha256,
            "created_time": self.created_time.isoformat() if self.created_time else None,
            "modified_time": self.modified_time.isoformat() if self.modified_time else None,
            "accessed_time": self.accessed_time.isoformat() if self.accessed_time else None,
            "file_owner": self.file_owner,
            "language": self.language,
            "document_id": self.document_id,
            "validation_report": {
                "is_valid": self.validation_report.is_valid,
                "issues": self.validation_report.issues,
            },
            "source_hash": self.source_hash,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "DocumentMetadata":
        validation_report = ValidationReport(
            is_valid=bool(payload.get("validation_report", {}).get("is_valid", False)),
            issues=list(payload.get("validation_report", {}).get("issues", [])),
        )
        return cls(
            file_name=payload["file_name"],
            absolute_path=Path(payload["absolute_path"]),
            relative_path=payload["relative_path"],
            extension=payload["extension"],
            mime_type=payload["mime_type"],
            file_size_bytes=int(payload["file_size_bytes"]),
            sha256=payload["sha256"],
            created_time=cls._parse_datetime(payload.get("created_time")),
            modified_time=cls._parse_datetime(payload.get("modified_time")),
            accessed_time=cls._parse_datetime(payload.get("accessed_time")),
            file_owner=payload.get("file_owner"),
            language=payload.get("language", "unknown"),
            document_id=payload["document_id"],
            validation_report=validation_report,
            source_hash=payload.get("source_hash"),
        )

    @staticmethod
    def _parse_datetime(value: Any) -> datetime | None:
        if not value:
            return None
        if isinstance(value, datetime):
            return value
        return datetime.fromisoformat(str(value))

    def is_duplicate_of(self, other: "DocumentMetadata") -> bool:
        return self.sha256 and other.sha256 and self.sha256 == other.sha256
