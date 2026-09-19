import json
import httpx
import pytest
from app.llm.errors import (
    LLMAuthenticationError,
    LLMConfigurationError,
    LLMRateLimitError,
    LLMValidationError,
)
from app.llm.models import LLMRequirementCandidate
from app.llm.providers.openai import OpenAICompatibleProvider


@pytest.mark.asyncio
async def test_openai_provider_missing_key_raises_config_error():
    provider = OpenAICompatibleProvider(api_key="")
    with pytest.raises(LLMConfigurationError, match="API key must be configured"):
        await provider.generate_structured("prompt", LLMRequirementCandidate)


@pytest.mark.asyncio
async def test_openai_provider_success_structured():
    mock_payload = {
        "choices": [
            {
                "message": {
                    "content": json.dumps({
                        "suggested_intent": "Manage users and permissions",
                        "suggested_actions": ["create", "update"],
                        "suggested_entities": ["User"],
                        "suggested_concepts": ["User Directory"],
                        "suggested_assumptions": ["Authentication via OAuth2"],
                        "suggested_clarifications": ["Should passwords expire?"],
                    })
                },
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": 100,
            "completion_tokens": 50,
            "total_tokens": 150,
        },
    }

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["authorization"] == "Bearer test-key"
        assert request.headers["content-type"] == "application/json"
        return httpx.Response(200, json=mock_payload)

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as client:
        provider = OpenAICompatibleProvider(api_key="test-key", client=client)
        candidate, metadata = await provider.generate_structured(
            prompt="Analyze requirement",
            response_model=LLMRequirementCandidate,
        )

        assert candidate.suggested_intent == "Manage users and permissions"
        assert "User" in candidate.suggested_entities
        assert metadata.provider == "openai"
        assert metadata.enhanced is True
        assert metadata.fallback_used is False
        assert metadata.usage is not None
        assert metadata.usage.total_tokens == 150


@pytest.mark.asyncio
async def test_openai_provider_401_auth_error():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(401, text="Unauthorized: Invalid API key")

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as client:
        provider = OpenAICompatibleProvider(api_key="bad-key", client=client)
        with pytest.raises(LLMAuthenticationError):
            await provider.generate_structured("prompt", LLMRequirementCandidate)


@pytest.mark.asyncio
async def test_openai_provider_429_rate_limit():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(429, text="Rate limit reached")

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as client:
        provider = OpenAICompatibleProvider(api_key="test-key", max_retries=1, client=client)
        with pytest.raises(LLMRateLimitError):
            await provider.generate_structured("prompt", LLMRequirementCandidate)


@pytest.mark.asyncio
async def test_openai_provider_invalid_json_validation_error():
    mock_payload = {
        "choices": [
            {
                "message": {
                    "content": "This is raw text, not valid JSON object"
                }
            }
        ]
    }

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=mock_payload)

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as client:
        provider = OpenAICompatibleProvider(api_key="test-key", client=client)
        with pytest.raises(LLMValidationError):
            await provider.generate_structured("prompt", LLMRequirementCandidate)
