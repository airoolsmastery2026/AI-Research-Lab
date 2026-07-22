"""Embedding engine for AI Librarian."""

from .batching import BatchProcessor
from .cache import EmbeddingCache
from .chunker import Chunk, ChunkingConfig, ChunkStrategy
from .manager import EmbeddingManager
from .models import EmbeddingRequest, EmbeddingResult
from .normalizer import normalize_vector
from .providers.base import BaseEmbeddingProvider
from .providers.gemini import GeminiProvider
from .providers.ollama import OllamaProvider
from .providers.openai import OpenAIProvider
from .providers.sentence_transformers import SentenceTransformersProvider
from .registry import ProviderRegistry
from .similarity import cosine_similarity, dot_product
from .splitter import RecursiveTextSplitter, MarkdownTextSplitter, CodeTextSplitter
from .tokenizer import count_tokens

__all__ = [
    "BatchProcessor",
    "Chunk",
    "ChunkingConfig",
    "ChunkStrategy",
    "EmbeddingCache",
    "EmbeddingManager",
    "EmbeddingRequest",
    "EmbeddingResult",
    "GeminiProvider",
    "MarkdownTextSplitter",
    "OllamaProvider",
    "OpenAIProvider",
    "ProviderRegistry",
    "RecursiveTextSplitter",
    "CodeTextSplitter",
    "SentenceTransformersProvider",
    "BaseEmbeddingProvider",
    "cosine_similarity",
    "dot_product",
    "normalize_vector",
    "count_tokens",
]
