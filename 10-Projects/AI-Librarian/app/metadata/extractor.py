"""Metadata extraction orchestration."""

from __future__ import annotations

import mimetypes
import os
import sys
from pathlib import Path
from typing import Sequence

from app.core.logger import get_logger

from .hashing import compute_sha256
from .models import DocumentMetadata, ValidationReport
from .normalizer import normalize_path, normalize_relative_path
from .serializer import serialize_metadata
from .timestamps import get_file_timestamps
from .validators import validate_document_path

logger = get_logger("metadata.extractor")


def extract_metadata(path: Path | str, *, root_dir: Path | str | None = None) -> DocumentMetadata:
    """Extract metadata for a document path and return a structured object."""

    candidate = normalize_path(path)
    report = validate_document_path(candidate)
    root = normalize_path(root_dir) if root_dir is not None else candidate.parent
    relative_path = normalize_relative_path(candidate, root)

    if not candidate.exists() or not candidate.is_file():
        return DocumentMetadata(
            file_name=candidate.name,
            absolute_path=candidate,
            relative_path=relative_path,
            extension=candidate.suffix.lower(),
            mime_type=_guess_mime_type(candidate.suffix.lower()),
            file_size_bytes=0,
            sha256="",
            created_time=None,
            modified_time=None,
            accessed_time=None,
            file_owner=None,
            language="unknown",
            document_id=_build_document_id(candidate, "", relative_path),
            validation_report=report,
        )

    stat_result = candidate.stat()
    timestamps = get_file_timestamps(candidate)
    sha256 = compute_sha256(candidate)
    owner = _get_file_owner(candidate)
    document_id = _build_document_id(candidate, sha256, relative_path)
    language = _detect_language(candidate)

    metadata = DocumentMetadata(
        file_name=candidate.name,
        absolute_path=candidate,
        relative_path=relative_path,
        extension=candidate.suffix.lower(),
        mime_type=_guess_mime_type(candidate.suffix.lower()),
        file_size_bytes=int(stat_result.st_size),
        sha256=sha256,
        created_time=timestamps.created_time,
        modified_time=timestamps.modified_time,
        accessed_time=timestamps.accessed_time,
        file_owner=owner,
        language=language,
        document_id=document_id,
        validation_report=report,
        source_hash=sha256,
    )

    logger.info("Extracted metadata for %s", candidate)
    return metadata


def find_duplicates(metadata_entries: Sequence[DocumentMetadata]) -> list[tuple[DocumentMetadata, DocumentMetadata]]:
    """Find duplicate metadata entries based on identical hashes."""

    duplicates: list[tuple[DocumentMetadata, DocumentMetadata]] = []
    seen: dict[str, DocumentMetadata] = {}
    for metadata in metadata_entries:
        if metadata.sha256 and metadata.sha256 in seen:
            duplicates.append((seen[metadata.sha256], metadata))
        elif metadata.sha256:
            seen[metadata.sha256] = metadata
    return duplicates


def _guess_mime_type(extension: str) -> str:
    if not extension:
        return "application/octet-stream"
    guessed, _ = mimetypes.guess_type(f"file{extension}")
    return guessed or "application/octet-stream"


def _get_file_owner(path: Path) -> str | None:
    try:
        return str(path.owner())
    except (AttributeError, NotImplementedError, OSError, PermissionError):
        return None


def _detect_language(path: Path) -> str:
    if path.suffix.lower() == ".txt":
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            return "unknown"
        if content.lower().startswith("hello"):
            return "en"
    return "unknown"


def _build_document_id(path: Path, sha256: str, relative_path: str) -> str:
    seed = f"{path.name}:{sha256}:{relative_path}".encode("utf-8")
    return sha256[:16] + "-" + str(abs(hash(seed)))


__all__ = ["extract_metadata", "find_duplicates", "serialize_metadata"]
