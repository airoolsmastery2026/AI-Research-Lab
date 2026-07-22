import pytest

from app.embedding import (
    Chunk,
    ChunkingConfig,
    EmbeddingCache,
    EmbeddingManager,
    EmbeddingRequest,
    EmbeddingResult,
    OpenAIProvider,
    SentenceTransformersProvider,
    cosine_similarity,
    dot_product,
    normalize_vector,
)


def test_sentence_chunking_with_overlap():
    text = "Alpha beta gamma delta epsilon zeta. Eta theta iota kappa lambda. Mu nu xi omicron."
    config = ChunkingConfig(chunk_size=8, overlap=2, strategy="sentence")
    chunks = EmbeddingManager.chunk_text(text, config)

    assert len(chunks) >= 2
    assert all(isinstance(chunk, Chunk) for chunk in chunks)
    assert chunks[0].text.startswith("Alpha")
    assert chunks[0].metadata["strategy"] == "sentence"


def test_recursive_and_markdown_splitters():
    text = "# Heading\n\nParagraph one. Paragraph two.\n\n```python\nprint('hi')\n```"
    config = ChunkingConfig(chunk_size=12, overlap=0, strategy="recursive")
    chunks = EmbeddingManager.chunk_text(text, config)

    assert any("Heading" in chunk.text for chunk in chunks)
    assert any("print('hi')" in chunk.text for chunk in chunks)


def test_embedding_manager_uses_cache_and_preserves_metadata():
    provider = OpenAIProvider()
    cache = EmbeddingCache()
    manager = EmbeddingManager(provider=provider, cache=cache)

    request = EmbeddingRequest(texts=["Alpha beta", "Alpha beta"], metadata={"doc_id": "doc-1"})
    results = manager.embed(request)

    assert len(results) == 2
    assert all(isinstance(result, EmbeddingResult) for result in results)
    assert results[0].embedding is not None
    assert results[0].metadata["doc_id"] == "doc-1"
    assert cache.get("Alpha beta") is not None


def test_similarity_and_normalization():
    a = [1.0, 0.0, 1.0]
    b = [0.0, 1.0, 1.0]

    assert pytest.approx(cosine_similarity(a, b)) == 0.5
    assert dot_product(a, b) == 1.0
    assert normalize_vector([3.0, 4.0])[0] == pytest.approx(0.6)


def test_sentence_transformers_provider_supports_batching():
    provider = SentenceTransformersProvider()
    response = provider.embed_batch(["one", "two"])

    assert len(response) == 2
    assert all(len(item.embedding) > 0 for item in response)


def test_duplicate_detection_and_streaming():
    manager = EmbeddingManager(provider=OpenAIProvider())
    texts = ["same text", "same text", "other"]

    deduped = manager.deduplicate(texts)
    assert deduped == ["same text", "other"]

    streamed = list(manager.stream_embeddings(texts))
    assert len(streamed) == len(texts)
