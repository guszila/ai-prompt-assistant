from typing import Any, AsyncIterator, Optional, Tuple, Type, TypeVar
from pydantic import BaseModel
from app.llm.base import BaseLLMProvider, LLMResponse, ModelInfo
from app.llm.errors import LLMError
from app.llm.models import LLMMetadata, LLMRequirementCandidate, LLMUsage

T = TypeVar("T", bound=BaseModel)


class MockLLMProvider(BaseLLMProvider):
    """
    Deterministic Mock LLM Provider for unit testing and offline development.
    Can be configured to return specific candidates or simulate specific failure modes.
    """

    def __init__(
        self,
        model_name: str = "mock-model-v1",
        programmed_candidate: Optional[LLMRequirementCandidate] = None,
        programmed_error: Optional[LLMError] = None,
    ):
        self._model_name = model_name
        self.programmed_candidate = programmed_candidate
        self.programmed_error = programmed_error

    @property
    def provider_name(self) -> str:
        return "mock"

    async def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs: Any) -> LLMResponse:
        if self.programmed_error:
            raise self.programmed_error

        return LLMResponse(
            content='{"suggested_intent": "Mock intent", "suggested_actions": ["view"]}',
            model_name=self._model_name,
            provider_name=self.provider_name,
            tokens_used=42,
            finish_reason="stop",
        )

    async def generate_structured(
        self,
        prompt: str,
        response_model: Type[T],
        system_prompt: Optional[str] = None,
        **kwargs: Any,
    ) -> Tuple[T, LLMMetadata]:
        if self.programmed_error:
            raise self.programmed_error

        metadata = LLMMetadata(
            provider=self.provider_name,
            model=self._model_name,
            enhanced=True,
            fallback_used=False,
            fallback_reason=None,
            latency_ms=12.5,
            usage=LLMUsage(prompt_tokens=25, completion_tokens=18, total_tokens=43),
        )

        if self.programmed_candidate and response_model == LLMRequirementCandidate:
            return self.programmed_candidate, metadata  # type: ignore

        # Default fallback mock candidate
        candidate = response_model(
            suggested_intent="Mock intent enhancement",
            suggested_actions=[],
            suggested_entities=[],
            suggested_concepts=[],
            suggested_assumptions=["Mock assumption requiring user confirmation"],
            suggested_clarifications=[],
        )
        return candidate, metadata

    async def generate_stream(
        self, prompt: str, system_prompt: Optional[str] = None, **kwargs: Any
    ) -> AsyncIterator[str]:
        if self.programmed_error:
            raise self.programmed_error

        chunks = ["{", '"suggested_intent":', ' "Mock intent"}']
        for chunk in chunks:
            yield chunk

    async def get_model_info(self) -> ModelInfo:
        return ModelInfo(
            provider=self.provider_name,
            model_name=self._model_name,
            is_local=True,
            context_window=8192,
            supports_streaming=True,
        )
