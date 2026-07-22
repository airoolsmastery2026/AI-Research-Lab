import pytest

from app.vectorstore import (
    FilterCriteria,
    MemoryVectorStore,
    SearchRequest,
    SearchResult,
    VectorStoreManager,
    VectorStoreError,
)


def test_memory_store_insert_search_and_delete():
    store = MemoryVectorStore(namespace="demo")
    store.upsert("doc-1", [0.1, 0.2, 0.3], {"source": "doc"})
    store.upsert("doc-2", [0.2, 0.3, 0.4], {"source": "wiki"})

    results = store.search(SearchRequest(query_vector=[0.1, 0.2, 0.3], top_k=2))
    assert len(results) == 2
    assert results[0].id == "doc-1"

    filtered = store.search(SearchRequest(query_vector=[0.1, 0.2, 0.3], top_k=2, filters=FilterCriteria(metadata={"source": "wiki"})))
    assert filtered[0].id == "doc-2"

    store.delete("doc-1")
    assert store.get("doc-1") is None


def test_manager_persists_and_exports_imports():
    store = MemoryVectorStore(namespace="demo")
    manager = VectorStoreManager(store)
    manager.upsert("doc-3", [1.0, 0.0, 0.0], {"source": "test"})

    exported = manager.export_data()
    assert exported["namespace"] == "demo"
    assert len(exported["items"]) == 1

    new_manager = VectorStoreManager(MemoryVectorStore(namespace="demo"))
    new_manager.import_data(exported)
    assert new_manager.get("doc-3") is not None


def test_vectorstore_error_and_stats():
    store = MemoryVectorStore(namespace="demo")
    with pytest.raises(VectorStoreError):
        store.search(SearchRequest(query_vector=[0.0, 0.0, 0.0], top_k=0))

    store.upsert("x", [0.0, 0.0, 0.0], {})
    stats = store.stats()
    assert stats["count"] >= 1
