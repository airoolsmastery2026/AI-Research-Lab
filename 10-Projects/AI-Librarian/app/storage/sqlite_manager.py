"""Helper for creating and maintaining SQLite schema objects."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable

from .database import DatabaseManager


class SQLiteManager:
    """Creates tables and indexes needed by the storage layer."""

    def __init__(self, database_manager: DatabaseManager) -> None:
        self.database_manager = database_manager

    def initialize_schema(self) -> None:
        with self.database_manager.get_connection() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS documents (
                    id TEXT PRIMARY KEY,
                    document_id TEXT NOT NULL UNIQUE,
                    title TEXT,
                    file_path TEXT NOT NULL,
                    extension TEXT,
                    mime_type TEXT,
                    size_bytes INTEGER,
                    sha256 TEXT,
                    created_at TEXT,
                    updated_at TEXT,
                    metadata_json TEXT
                );

                CREATE TABLE IF NOT EXISTS metadata_entries (
                    id TEXT PRIMARY KEY,
                    document_id TEXT NOT NULL,
                    key_name TEXT NOT NULL,
                    value_text TEXT,
                    FOREIGN KEY(document_id) REFERENCES documents(document_id)
                );

                CREATE TABLE IF NOT EXISTS chunks (
                    id TEXT PRIMARY KEY,
                    document_id TEXT NOT NULL,
                    index_number INTEGER NOT NULL,
                    text_content TEXT NOT NULL,
                    metadata_json TEXT,
                    FOREIGN KEY(document_id) REFERENCES documents(document_id)
                );

                CREATE TABLE IF NOT EXISTS embeddings (
                    id TEXT PRIMARY KEY,
                    document_id TEXT NOT NULL,
                    vector_json TEXT NOT NULL,
                    metadata_json TEXT,
                    FOREIGN KEY(document_id) REFERENCES documents(document_id)
                );

                CREATE TABLE IF NOT EXISTS history (
                    id TEXT PRIMARY KEY,
                    document_id TEXT NOT NULL,
                    action TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    details TEXT
                );

                CREATE INDEX IF NOT EXISTS idx_documents_document_id ON documents(document_id);
                CREATE INDEX IF NOT EXISTS idx_chunks_document_id ON chunks(document_id);
                CREATE INDEX IF NOT EXISTS idx_embeddings_document_id ON embeddings(document_id);
                """
            )
