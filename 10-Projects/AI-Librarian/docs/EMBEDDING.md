# Embedding Engine

The embedding engine provides chunking, normalization, similarity, caching, batching, and provider abstraction for AI Librarian.

## Features
- Sentence, recursive, markdown, and code chunking
- Token-aware chunking via simple estimators
- Overlap support
- Embedding cache
- Batch processing
- Provider abstraction for OpenAI, Gemini, SentenceTransformers, and Ollama
- Cosine similarity and dot-product helpers
- Duplicate detection and streaming support

## Usage
```python
from app.embedding import EmbeddingManager, EmbeddingRequest, ChunkingConfig

manager = EmbeddingManager()
request = EmbeddingRequest(texts=["Hello world"])
results = manager.embed(request)
```
