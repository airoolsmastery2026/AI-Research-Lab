import pytest

from app.llm import (
    CompletionRequest,
    CompletionResponse,
    LLMConfigurationError,
    LLMManager,
    ModelRegistry,
    ProviderFactory,
)
from app.llm.models import ModelConfig, ProviderConfig
from app.llm.providers import AnthropicProvider, GeminiProvider, OllamaProvider, OpenAIProvider, OpenRouterProvider


def test_provider_factory_creates_supported_providers():
    assert isinstance(ProviderFactory.create("openai"), OpenAIProvider)
    assert isinstance(ProviderFactory.create("gemini"), GeminiProvider)
    assert isinstance(ProviderFactory.create("openrouter"), OpenRouterProvider)
    assert isinstance(ProviderFactory.create("anthropic"), AnthropicProvider)
    assert isinstance(ProviderFactory.create("ollama"), OllamaProvider)


def test_provider_factory_rejects_unknown_provider():
    with pytest.raises(LLMConfigurationError):
        ProviderFactory.create("unknown")


def test_manager_completes_with_registered_provider():
    manager = LLMManager()
    manager.register_provider("openai", ProviderConfig(name="openai", api_key="test-key"))
    manager.register_model("gpt-test", "openai")

    response = manager.complete(CompletionRequest(model="gpt-test", prompt="Hello"), provider_name="openai")

    assert response.provider == "openai"
    assert response.text.startswith("OpenAI stub response")
    assert response.total_tokens > 0


def test_context_and_registry_work():
    registry = ModelRegistry()
    registry.register(ModelConfig(name="demo", provider="openai"))

    assert registry.get("demo") is not None
    assert len(registry.list_models()) == 1


def test_completion_response_can_be_created():
    response = CompletionResponse(text="done", model="m", provider="p")
    assert response.text == "done"
