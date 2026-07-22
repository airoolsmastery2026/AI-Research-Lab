"""Registry of available model configurations."""

from __future__ import annotations

from .models import ModelConfig


class ModelRegistry:
    """Simple in-memory registry for supported models."""

    def __init__(self) -> None:
        self._models: dict[str, ModelConfig] = {}

    def register(self, model: ModelConfig) -> None:
        self._models[model.name] = model

    def get(self, name: str) -> ModelConfig | None:
        return self._models.get(name)

    def list_models(self) -> list[ModelConfig]:
        return list(self._models.values())
