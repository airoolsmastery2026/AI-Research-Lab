"""Typed configuration and request/response models for the LLM layer."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass(slots=True)
class ProviderConfig:
    name: str
    api_key: str | None = None
    base_url: str | None = None
    timeout_seconds: int = 30
    max_retries: int = 3
    rate_limit_per_minute: int = 60
    model: str | None = None


@dataclass(slots=True)
class ModelConfig:
    name: str
    provider: str
    max_tokens: int = 4096
    cost_per_1k_tokens: float = 0.0


@dataclass(slots=True)
class CompletionRequest:
    model: str
    prompt: str
    system_prompt: str | None = None
    temperature: float = 0.2
    max_tokens: int = 512
    json_mode: bool = False
    stream: bool = False
    tools: list[dict[str, Any]] = field(default_factory=list)


@dataclass(slots=True)
class CompletionResponse:
    text: str
    model: str
    provider: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    cost_usd: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)
