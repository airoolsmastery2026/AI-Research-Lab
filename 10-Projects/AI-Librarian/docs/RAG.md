# RAG Engine

The RAG engine provides a production-ready retrieval and generation pipeline for AI Librarian using the existing metadata, importer, parser, storage, embedding, vector store, and LLM subsystems.

## Features
- Hybrid search and dense/keyword retrieval
- Context window management
- Conversation memory and history compression
- Query rewriting and reranking
- Prompt templates and citation generation
- Streaming response support
- Evaluation metrics and latency tracking

## Usage
```python
from app.rag import RAGManager, AnswerRequest

manager = RAGManager()
response = manager.answer(AnswerRequest(question="What is AI?"))
print(response.answer)
```
