# Storage Layer

The storage layer provides the persistence backbone for AI Librarian through SQLite-backed repositories, caches, indexing, backup, and versioning.

## Components

- Database manager with SQLite connections and transactions
- Repository classes for documents, metadata, chunks, embeddings, and history
- Memory and disk caches
- Search index and registry helpers
- Backup and restore utilities
- Version management and migration hooks

## Usage

```python
from app.storage.database import DatabaseConfig, DatabaseManager
from app.storage.sqlite_manager import SQLiteManager
from app.storage.repositories.document_repository import DocumentRepository

manager = DatabaseManager(DatabaseConfig(path="./storage.db"))
SQLiteManager(manager).initialize_schema()
repository = DocumentRepository(manager)
```
