import asyncio
import json
import time
from typing import Any, AsyncIterator, Dict, Optional, Tuple, Type, TypeVar
import httpx
from pydantic import BaseModel, ValidationError
from app.llm.base import BaseLLMProvider, LLMResponse, ModelInfo
from app.llm.errors import (
    LLMAuthenticationError,
    LLMConfigurationError,
    LLMNetworkError,
    LLMRateLimitError,
    LLMTimeoutError,
    LLMValidationError,
)
from app.llm.models import LLMMetadata, LLMUsage

T = TypeVar("T", bound=BaseModel)


class OpenAICompatibleProvider(BaseLLMProvider):
    """
    Provider for standard OpenAI-compatible chat completion endpoints using httpx.
    Provides structured JSON generation, bounded retries, and strict error classification.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = "gpt-4o-mini",
        base_url: Optional[str] = None,
        timeout_seconds: float = 15.0,
        max_retries: int = 2,
        client: Optional[httpx.AsyncClient] = None,
    ):
        self._api_key = api_key
        self._model_name = model_name
        self._base_url = (base_url or "https://api.openai.com/v1").rstrip("/")
        self._timeout_seconds = timeout_seconds
        self._max_retries = max_retries
        self._client = client

    @property
    def provider_name(self) -> str:
        return "openai"

    def _get_headers(self) -> Dict[str, str]:
        if not self._api_key or not self._api_key.strip():
            raise LLMConfigurationError("API key must be configured for OpenAI provider.")
        return {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    async def _post_chat_completions(self, payload: Dict[str, Any]) -> Tuple[Dict[str, Any], float]:
        """Execute chat completions with bounded retries and exponential backoff."""
        headers = self._get_headers()
        url = f"{self._base_url}/chat/completions"
        timeout = httpx.Timeout(self._timeout_seconds)

        start_time = time.perf_counter()
        last_exception: Optional[Exception] = None

        for attempt in range(self._max_retries + 1):
            try:
                # Use injected client (for tests) or create dedicated context
                if self._client:
                    response = await self._client.post(url, json=payload, headers=headers, timeout=timeout)
                else:
                    async with httpx.AsyncClient() as client:
                        response = await client.post(url, json=payload, headers=headers, timeout=timeout)

                elapsed_ms = (time.perf_counter() - start_time) * 1000.0

                if response.status_code == 200:
                    return response.json(), elapsed_ms
                elif response.status_code in (401, 403):
                    raise LLMAuthenticationError(
                        f"Authentication failed with status {response.status_code}: {response.text}"
                    )
                elif response.status_code == 429:
                    if attempt < self._max_retries:
                        await asyncio.sleep(0.5 * (2**attempt))
                        continue
                    raise LLMRateLimitError(f"Rate limit exceeded: {response.text}")
                elif response.status_code in (500, 502, 503, 504):
                    if attempt < self._max_retries:
                        await asyncio.sleep(0.5 * (2**attempt))
                        continue
                    raise LLMNetworkError(f"Provider server error {response.status_code}: {response.text}")
                else:
                    raise LLMConfigurationError(f"Provider rejected request with HTTP {response.status_code}: {response.text}")

            except httpx.TimeoutException as exc:
                last_exception = exc
                if attempt < self._max_retries:
                    await asyncio.sleep(0.5 * (2**attempt))
                    continue
                raise LLMTimeoutError(f"Request timed out after {self._timeout_seconds}s: {str(exc)}") from exc
            except httpx.NetworkError as exc:
                last_exception = exc
                if attempt < self._max_retries:
                    await asyncio.sleep(0.5 * (2**attempt))
                    continue
                raise LLMNetworkError(f"Network error connecting to provider: {str(exc)}") from exc

        if last_exception:
            raise LLMNetworkError(f"Provider call failed after retries: {str(last_exception)}") from last_exception
        raise LLMNetworkError("Provider call failed without response")

    async def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs: Any) -> LLMResponse:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self._model_name,
            "messages": messages,
            "temperature": kwargs.get("temperature", 0.2),
            "max_tokens": kwargs.get("max_tokens", 2048),
        }

        data, _ = await self._post_chat_completions(payload)
        choice = data.get("choices", [{}])[0]
        content = choice.get("message", {}).get("content", "")
        finish_reason = choice.get("finish_reason")
        tokens_used = data.get("usage", {}).get("total_tokens")

        return LLMResponse(
            content=content,
            model_name=self._model_name,
            provider_name=self.provider_name,
            tokens_used=tokens_used,
            finish_reason=finish_reason,
        )

    async def generate_structured(
        self,
        prompt: str,
        response_model: Type[T],
        system_prompt: Optional[str] = None,
        **kwargs: Any,
    ) -> Tuple[T, LLMMetadata]:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self._model_name,
            "messages": messages,
            "temperature": kwargs.get("temperature", 0.2),
            "max_tokens": kwargs.get("max_tokens", 2048),
            "response_format": {"type": "json_object"},
        }

        data, latency_ms = await self._post_chat_completions(payload)
        choice = data.get("choices", [{}])[0]
        raw_content = choice.get("message", {}).get("content", "")

        raw_usage = data.get("usage", {})
        usage = LLMUsage(
            prompt_tokens=raw_usage.get("prompt_tokens", 0),
            completion_tokens=raw_usage.get("completion_tokens", 0),
            total_tokens=raw_usage.get("total_tokens", 0),
        )

        metadata = LLMMetadata(
            provider=self.provider_name,
            model=self._model_name,
            enhanced=True,
            fallback_used=False,
            fallback_reason=None,
            latency_ms=round(latency_ms, 2),
            usage=usage,
        )

        try:
            parsed_json = json.loads(raw_content)
            candidate = response_model.model_validate(parsed_json)
            return candidate, metadata
        except (json.JSONDecodeError, ValidationError) as exc:
            raise LLMValidationError(f"Failed to validate response against {response_model.__name__}: {str(exc)}") from exc

    async def generate_stream(
        self, prompt: str, system_prompt: Optional[str] = None, **kwargs: Any
    ) -> AsyncIterator[str]:
        """Streaming chat completions via Server-Sent Events."""
        headers = self._get_headers()
        url = f"{self._base_url}/chat/completions"
        timeout = httpx.Timeout(self._timeout_seconds)

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self._model_name,
            "messages": messages,
            "temperature": kwargs.get("temperature", 0.2),
            "stream": True,
        }

        async with httpx.AsyncClient() as client:
            async with client.stream("POST", url, json=payload, headers=headers, timeout=timeout) as response:
                if response.status_code != 200:
                    raise LLMNetworkError(f"Streaming failed with HTTP {response.status_code}")
                async for line in response.aiter_lines():
                    if line.startswith("data: ") and line != "data: [DONE]":
                        try:
                            chunk_data = json.loads(line[6:])
                            delta = chunk_data.get("choices", [{}])[0].get("delta", {}).get("content", "")
                            if delta:
                                yield delta
                        except json.JSONDecodeError:
                            continue

    async def get_model_info(self) -> ModelInfo:
        return ModelInfo(
            provider=self.provider_name,
            model_name=self._model_name,
            is_local=False,
            context_window=128000,
            supports_streaming=True,
        )
