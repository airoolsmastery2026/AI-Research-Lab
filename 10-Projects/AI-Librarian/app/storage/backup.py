"""Backup and restore utilities for the storage layer."""

from __future__ import annotations

import shutil
from pathlib import Path

from app.core.logger import get_logger

from .database import DatabaseManager
from .errors import StorageError

logger = get_logger("storage.backup")


class BackupManager:
    """Create and restore backups of the SQLite database file."""

    def __init__(self, database_manager: DatabaseManager) -> None:
        self.database_manager = database_manager

    def backup(self, destination: Path | str) -> Path:
        destination_path = Path(destination).expanduser().resolve()
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        source_path = self.database_manager.config.path
        if not source_path.exists():
            raise StorageError(f"Database file does not exist: {source_path}")
        shutil.copy2(source_path, destination_path)
        logger.info("Backed up database to %s", destination_path)
        return destination_path

    def restore(self, backup_path: Path | str) -> Path:
        backup_file = Path(backup_path).expanduser().resolve()
        if not backup_file.exists():
            raise StorageError(f"Backup file does not exist: {backup_file}")
        destination = self.database_manager.config.path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(backup_file, destination)
        logger.info("Restored database from %s", backup_file)
        return destination
