"""Metadata engine package."""

from .extractor import extract_metadata, find_duplicates
from .hashing import compute_sha256
from .models import DocumentMetadata, ValidationReport
from .normalizer import normalize_path, normalize_relative_path
from .serializer import serialize_metadata
from .timestamps import get_file_timestamps
from .validators import validate_document_path

__all__ = [
    "DocumentMetadata",
    "ValidationReport",
    "compute_sha256",
    "extract_metadata",
    "find_duplicates",
    "normalize_path",
    "normalize_relative_path",
    "serialize_metadata",
    "validate_document_path",
    "get_file_timestamps",
]
