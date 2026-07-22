"""Vector store subsystem for AI Librarian."""

from .base import BaseVectorStore, VectorRecord
from .errors import VectorStoreError
from .filters import FilterCriteria
from .manager import VectorStoreManager
from .memory_store import MemoryVectorStore
from .metrics import VectorStoreMetrics
from .search import SearchRequest, SearchResult
from .serializer import serialize_record, deserialize_record

__all__ = [
    "BaseVectorStore",
    "FilterCriteria",
    "MemoryVectorStore",
    "SearchRequest",
    "SearchResult",
    "VectorRecord",
    "VectorStoreError",
    "VectorStoreManager",
    "VectorStoreMetrics",
    "serialize_record",
    "deserialize_record",
]
