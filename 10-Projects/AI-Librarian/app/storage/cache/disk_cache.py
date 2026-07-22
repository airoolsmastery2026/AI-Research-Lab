"""Disk-backed cache implementation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class DiskCache:
    """Simple JSON-backed disk cache."""

    def __init__(self, root_dir: Path | str) -> None:
        self.root_dir = Path(root_dir).expanduser().resolve()
        self.root_dir.mkdir(parents=True, exist_ok=True)

    def get(self, key: str) -> Any | None:
        path = self.root_dir / f"{key}.json"
        if not path.exists():
            return None
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def set(self, key: str, value: Any) -> None:
        path = self.root_dir / f"{key}.json"
        with path.open("w", encoding="utf-8") as handle:
            json.dump(value, handle, sort_keys=True)

    def delete(self, key: str) -> None:
        path = self.root_dir / f"{key}.json"
        if path.exists():
            path.unlink()
