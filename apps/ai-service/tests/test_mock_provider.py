import pytest
from app.llm.base import BaseLLMProvider
from app.llm.errors import LLMTimeoutError
from app.llm.models import LLMRequirementCandidate
from app.llm.providers.mock import MockLLMProvider


@pytest.mark.asyncio
async def test_mock_provider_contract():
    provider = MockLLMProvider(model_name="test-mock")
    assert isinstance(provider, BaseLLMProvider)
    assert provider.provider_name == "mock"

    info = await provider.get_model_info()
    assert info.model_name == "test-mock"
    assert info.supports_streaming is True


@pytest.mark.asyncio
async def test_mock_provider_generate():
    provider = MockLLMProvider()
    resp = await provider.generate("Test prompt")
    assert resp.model_name == "mock-model-v1"
    assert resp.content != ""


@pytest.mark.asyncio
async def test_mock_provider_generate_structured():
    candidate_data = LLMRequirementCandidate(
        suggested_intent="Programmable intent",
        suggested_actions=["create", "view"],
        suggested_entities=["Product"],
        suggested_concepts=["Product Catalog"],
        suggested_assumptions=["Images are hosted on S3"],
        suggested_clarifications=["Are thumbnail images required?"],
    )
    provider = MockLLMProvider(programmed_candidate=candidate_data)
    candidate, metadata = await provider.generate_structured(
        prompt="Analyze product catalog",
        response_model=LLMRequirementCandidate,
    )

    assert candidate.suggested_intent == "Programmable intent"
    assert "Product" in candidate.suggested_entities
    assert metadata.enhanced is True
    assert metadata.fallback_used is False
    assert metadata.fallback_reason is None
    assert metadata.latency_ms is not None
    assert metadata.usage is not None


@pytest.mark.asyncio
async def test_mock_provider_programmable_error():
    provider = MockLLMProvider(programmed_error=LLMTimeoutError("Simulation timeout"))
    with pytest.raises(LLMTimeoutError):
        await provider.generate("Test prompt")


@pytest.mark.asyncio
async def test_mock_provider_streaming():
    provider = MockLLMProvider()
    chunks = []
    async for chunk in provider.generate_stream("Stream prompt"):
        chunks.append(chunk)
    assert len(chunks) > 0
    assert "".join(chunks) != ""
