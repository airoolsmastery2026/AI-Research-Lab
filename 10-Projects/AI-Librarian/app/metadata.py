"""Compatibility module for the metadata engine."""

from app.metadata.extractor import extract_metadata, find_duplicates
from app.metadata.models import DocumentMetadata, ValidationReport
from app.metadata.serializer import serialize_metadata

__all__ = [
    "DocumentMetadata",
    "ValidationReport",
    "extract_metadata",
    "find_duplicates",
    "serialize_metadata",
]