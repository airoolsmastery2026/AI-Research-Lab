import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.storage.backup import BackupManager
from app.storage.cache.disk_cache import DiskCache
from app.storage.cache.memory_cache import MemoryCache
from app.storage.database import DatabaseConfig, DatabaseManager
from app.storage.index.registry import IndexRegistry
from app.storage.index.search_index import SearchIndex
from app.storage.models.chunk_record import ChunkRecord
from app.storage.models.document_record import DocumentRecord
from app.storage.models.embedding_record import EmbeddingRecord
from app.storage.repositories.chunk_repository import ChunkRepository
from app.storage.repositories.document_repository import DocumentRepository
from app.storage.repositories.embedding_repository import EmbeddingRepository
from app.storage.repositories.history_repository import HistoryEntry, HistoryRepository
from app.storage.sqlite_manager import SQLiteManager
from app.storage.versioning import VersionManager


def test_database_and_repository_round_trip(tmp_path):
    database_path = tmp_path / "storage.db"
    database_manager = DatabaseManager(DatabaseConfig(path=database_path))
    sqlite_manager = SQLiteManager(database_manager)
    sqlite_manager.initialize_schema()

    document_repository = DocumentRepository(database_manager)
    document_record = DocumentRecord(
        id="doc-1",
        document_id="doc-1",
        title="Sample",
        file_path="/tmp/sample.txt",
        extension=".txt",
        mime_type="text/plain",
        size_bytes=10,
        sha256="abc",
        created_at="2024-01-01",
        updated_at="2024-01-01",
    )
    document_repository.save(document_record)

    stored = document_repository.find_by_id("doc-1")
    assert stored.document_id == "doc-1"
    assert stored.title == "Sample"


def test_chunk_and_embedding_repositories(tmp_path):
    database_path = tmp_path / "storage.db"
    database_manager = DatabaseManager(DatabaseConfig(path=database_path))
    SQLiteManager(database_manager).initialize_schema()

    chunk_repository = ChunkRepository(database_manager)
    embedding_repository = EmbeddingRepository(database_manager)

    chunk_repository.save(ChunkRecord(id="chunk-1", document_id="doc-1", index_number=0, text_content="hello"))
    embedding_repository.save(EmbeddingRecord(id="embed-1", document_id="doc-1", vector=[0.1, 0.2]))

    chunks = chunk_repository.list_for_document("doc-1")
    embeddings = embedding_repository.list_for_document("doc-1")

    assert len(chunks) == 1
    assert len(embeddings) == 1


def test_history_cache_and_indexing(tmp_path):
    database_path = tmp_path / "storage.db"
    database_manager = DatabaseManager(DatabaseConfig(path=database_path))
    SQLiteManager(database_manager).initialize_schema()

    history_repository = HistoryRepository(database_manager)
    history_repository.save(HistoryEntry(id="history-1", document_id="doc-1", action="import", created_at="2024-01-01"))

    memory_cache = MemoryCache()
    memory_cache.set("doc-1", {"status": "ready"})

    disk_cache = DiskCache(tmp_path / "cache")
    disk_cache.set("doc-1", {"status": "ready"})

    registry = IndexRegistry()
    registry.register("documents")
    search_index = SearchIndex()
    search_index.add("doc-1", ["hello", "world"])

    assert history_repository.list_for_document("doc-1")[0].action == "import"
    assert memory_cache.get("doc-1")["status"] == "ready"
    assert disk_cache.get("doc-1")["status"] == "ready"
    assert search_index.search("hello") == ["doc-1"]
    assert registry.get("documents") is not None


def test_backup_and_versioning(tmp_path):
    database_path = tmp_path / "storage.db"
    database_manager = DatabaseManager(DatabaseConfig(path=database_path))
    SQLiteManager(database_manager).initialize_schema()

    backup_manager = BackupManager(database_manager)
    backup_path = backup_manager.backup(tmp_path / "backup.db")
    assert backup_path.exists()

    version_manager = VersionManager()
    version_manager.bump()
    assert version_manager.current_version == 2
