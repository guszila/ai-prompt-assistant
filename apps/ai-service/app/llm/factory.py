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
        # Lazy default registration if not already registered
        if provider_key == "mock":
            from app.llm.providers.mock import MockLLMProvider
            return MockLLMProvider()
        elif provider_key == "openai":
            from app.core.config import settings
            from app.llm.providers.openai import OpenAICompatibleProvider
            api_key = settings.LLM_API_KEY.get_secret_value() if settings.LLM_API_KEY else None
            return OpenAICompatibleProvider(
                api_key=api_key,
                model_name=settings.LLM_MODEL,
                base_url=settings.LLM_BASE_URL,
                timeout_seconds=settings.LLM_TIMEOUT_SECONDS,
                max_retries=settings.LLM_MAX_RETRIES,
            )

        raise ValueError(
            f"LLM Provider '{name}' is not registered. Available providers: {list(_registry.keys())}"
        )
    return _registry[provider_key]()
