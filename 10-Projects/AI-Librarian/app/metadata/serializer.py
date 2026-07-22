"""Serialization helpers for document metadata."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import DocumentMetadata


def serialize_metadata(metadata: DocumentMetadata) -> dict[str, Any]:
    """Serialize document metadata to a JSON-compatible dictionary."""

    return metadata.to_dict()


def write_metadata_json(metadata: DocumentMetadata, destination: Path | str) -> Path:
    """Write a metadata payload to disk as JSON."""

    destination_path = Path(destination).expanduser()
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    with destination_path.open("w", encoding="utf-8") as handle:
        json.dump(serialize_metadata(metadata), handle, indent=2, sort_keys=True)
    return destination_path
