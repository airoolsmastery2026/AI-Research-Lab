from app.rag import (
    AnswerRequest,
    ContextDocument,
    EvaluationResult,
    RAGManager,
    RetrievalResult,
    Retriever,
    Reranker,
    QueryRewriter,
    PromptBuilder,
    Citation,
    HybridSearch,
    StreamingResponse,
)


def test_rag_pipeline_builds_context_and_answers():
    manager = RAGManager()
    request = AnswerRequest(question="What is AI?", top_k=2)
    response = manager.answer(request)

    assert response.answer
    assert response.context_documents
    assert response.citations


def test_retriever_and_hybrid_search_return_results():
    retriever = Retriever()
    results = retriever.retrieve("AI research")
    assert len(results) >= 1

    hybrid = HybridSearch()
    hybrid_results = hybrid.search("AI research")
    assert len(hybrid_results) >= 1


def test_prompt_builder_and_rewriter_work():
    builder = PromptBuilder()
    prompt = builder.build("What is AI?")
    assert "What is AI?" in prompt

    rewriter = QueryRewriter()
    rewritten = rewriter.rewrite("What is AI?")
    assert rewritten


def test_reranker_and_evaluator_metrics():
    reranker = Reranker()
    ranked = reranker.rerank([RetrievalResult(doc_id="a", text="one", score=0.2), RetrievalResult(doc_id="b", text="two", score=0.9)])
    assert ranked[0].doc_id == "b"

    evaluator = EvaluationResult()
    assert evaluator.score == 0.0


def test_streaming_response_and_citation():
    citation = Citation(source="doc", page=1)
    assert citation.source == "doc"

    stream = StreamingResponse(chunks=["hello", "world"])
    assert stream.chunks == ["hello", "world"]
