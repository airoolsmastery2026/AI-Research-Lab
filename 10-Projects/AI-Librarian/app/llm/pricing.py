"""Pricing helpers for LLM models."""

from __future__ import annotations

from .models import CompletionResponse, ModelConfig


def calculate_cost(response: CompletionResponse, model_config: ModelConfig) -> float:
    """Estimate the USD cost of a completion response."""

    if model_config.cost_per_1k_tokens <= 0:
        return 0.0
    return round((response.total_tokens / 1000.0) * model_config.cost_per_1k_tokens, 6)
