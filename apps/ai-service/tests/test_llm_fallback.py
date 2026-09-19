import pytest
from app.domain.prompt import PromptRequest
from app.engine.pipeline import CorePromptEnginePipeline
from app.llm.errors import (
    LLMAuthenticationError,
    LLMRateLimitError,
    LLMTimeoutError,
    LLMValidationError,
)
from app.llm.models import LLMFallbackReason
from app.llm.providers.mock import MockLLMProvider
from tests.fixtures.requirements import REQ_THAI_CRUD


@pytest.mark.asyncio
async def test_fallback_on_timeout():
    provider = MockLLMProvider(programmed_error=LLMTimeoutError("Simulated timeout"))
    req = PromptRequest(raw_text=REQ_THAI_CRUD, enable_llm=True)

    result = await CorePromptEnginePipeline.execute_async(req, provider=provider)

    assert result.validation.is_valid is True
    assert result.llm_metadata is not None
    assert result.llm_metadata.enhanced is False
    assert result.llm_metadata.fallback_used is True
    assert result.llm_metadata.fallback_reason == LLMFallbackReason.TIMEOUT
    # Prompt is still complete with all M2 CRUD requirements
    assert len(result.prompt.requirements) >= 4


@pytest.mark.asyncio
async def test_fallback_on_authentication_error():
    provider = MockLLMProvider(programmed_error=LLMAuthenticationError("Simulated 401"))
    req = PromptRequest(raw_text=REQ_THAI_CRUD, enable_llm=True)

    result = await CorePromptEnginePipeline.execute_async(req, provider=provider)

    assert result.validation.is_valid is True
    assert result.llm_metadata is not None
    assert result.llm_metadata.fallback_used is True
    assert result.llm_metadata.fallback_reason == LLMFallbackReason.AUTHENTICATION_ERROR


@pytest.mark.asyncio
async def test_fallback_on_rate_limit():
    provider = MockLLMProvider(programmed_error=LLMRateLimitError("Simulated 429"))
    req = PromptRequest(raw_text=REQ_THAI_CRUD, enable_llm=True)

    result = await CorePromptEnginePipeline.execute_async(req, provider=provider)

    assert result.validation.is_valid is True
    assert result.llm_metadata is not None
    assert result.llm_metadata.fallback_used is True
    assert result.llm_metadata.fallback_reason == LLMFallbackReason.RATE_LIMIT


@pytest.mark.asyncio
async def test_fallback_on_validation_error():
    provider = MockLLMProvider(programmed_error=LLMValidationError("Simulated malformed JSON"))
    req = PromptRequest(raw_text=REQ_THAI_CRUD, enable_llm=True)

    result = await CorePromptEnginePipeline.execute_async(req, provider=provider)

    assert result.validation.is_valid is True
    assert result.llm_metadata is not None
    assert result.llm_metadata.fallback_used is True
    assert result.llm_metadata.fallback_reason == LLMFallbackReason.VALIDATION_ERROR


@pytest.mark.asyncio
async def test_disabled_llm_state():
    """When LLM is disabled, fallback_used is False and fallback_reason is None."""
    req = PromptRequest(raw_text=REQ_THAI_CRUD, enable_llm=False)

    result = await CorePromptEnginePipeline.execute_async(req)

    assert result.validation.is_valid is True
    assert result.llm_metadata is not None
    assert result.llm_metadata.enhanced is False
    assert result.llm_metadata.fallback_used is False
    assert result.llm_metadata.fallback_reason is None
