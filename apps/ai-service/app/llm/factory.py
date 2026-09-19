from typing import Callable, Dict
from app.llm.base import BaseLLMProvider

ProviderBuilder = Callable[[], BaseLLMProvider]

_registry: Dict[str, ProviderBuilder] = {}


def register_llm_provider(name: str, builder: ProviderBuilder) -> None:
    """Register an LLM provider builder dynamically."""
    _registry[name.lower()] = builder


def get_llm_provider(name: str) -> BaseLLMProvider:
    """Retrieve an instantiated LLM provider from the registry."""
    provider_key = name.lower()
    if provider_key not in _registry:
        raise ValueError(
            f"LLM Provider '{name}' is not registered. Available providers: {list(_registry.keys())}"
        )
    return _registry[provider_key]()
