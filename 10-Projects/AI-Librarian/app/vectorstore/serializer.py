"""Serialization helpers for vector records."""

from __future__ import annotations

from typing import Any

from .base import VectorRecord


def serialize_record(record: VectorRecord) -> dict[str, Any]:
    return {"id": record.id, "vector": record.vector, "metadata": record.metadata}


def deserialize_record(payload: dict[str, Any]) -> VectorRecord:
    return VectorRecord(id=payload["id"], vector=list(payload.get("vector", [])), metadata=dict(payload.get("metadata", {})))
