# Vector Store

The vector store subsystem provides a provider-agnostic repository interface for vector data with a simple in-memory backend and manager helpers.

## Features
- Provider abstraction and repository pattern
- Memory-backed persistence and import/export
- Top-k search with cosine similarity
- Metadata filtering and namespace support
- Incremental indexing helpers
- Batch insert/delete/update support through the manager interface

## Usage
```python
from app.vectorstore import MemoryVectorStore, VectorStoreManager, SearchRequest

store = MemoryVectorStore(namespace="demo")
manager = VectorStoreManager(store)
manager.upsert("doc-1", [0.1, 0.2, 0.3], {"source": "doc"})
results = manager.search(SearchRequest(query_vector=[0.1, 0.2, 0.3], top_k=3))
```
