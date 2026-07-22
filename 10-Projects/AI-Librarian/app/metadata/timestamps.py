"""Timestamp extraction utilities."""

from __future__ import annotations

import os
import platform
from datetime import datetime
from pathlib import Path
from typing import NamedTuple


class FileTimestamps(NamedTuple):
    created_time: datetime | None
    modified_time: datetime | None
    accessed_time: datetime | None


def get_file_timestamps(path: Path) -> FileTimestamps:
    """Return created, modified, and accessed times for the file."""

    stat_result = path.stat()
    created_time = _to_datetime(stat_result.st_ctime)
    modified_time = _to_datetime(stat_result.st_mtime)
    accessed_time = _to_datetime(stat_result.st_atime)
    return FileTimestamps(created_time, modified_time, accessed_time)


def _to_datetime(timestamp: float) -> datetime | None:
    if timestamp is None:
        return None
    return datetime.fromtimestamp(timestamp)
