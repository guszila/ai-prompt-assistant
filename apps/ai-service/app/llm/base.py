from abc import ABC, abstractmethod
from typing import Any, AsyncIterator, Dict, Optional
from pydantic import BaseModel, Field


class LLMResponse(BaseModel):
    """Standardized response from any LLM provider."""
    content: str
    model_name: str
    provider_name: str
    tokens_used: Optional[int] = None
    finish_reason: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ModelInfo(BaseModel):
    """Metadata describing a supported model."""
    provider: str
    model_name: str
    is_local: bool
    context_window: int
    supports_streaming: bool = True


class BaseLLMProvider(ABC):
    """
    Abstract interface for LLM providers.
    Decouples core application from specific cloud vendors and local runtimes.
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Name of the provider (e.g., anthropic, openai, gemini, ollama)."""
        pass

    @abstractmethod
    async def generate(self, prompt: str, **kwargs: Any) -> LLMResponse:
        """Generate a complete response for the given prompt."""
        pass

    @abstractmethod
    async def generate_stream(self, prompt: str, **kwargs: Any) -> AsyncIterator[str]:
        """Stream chunks of response text for the given prompt."""
        pass

    @abstractmethod
    async def get_model_info(self) -> ModelInfo:
        """Return information and capabilities of the configured model."""
        pass
