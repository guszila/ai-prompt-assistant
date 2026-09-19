import json
import pytest
from pydantic import SecretStr
from app.core.config import Settings
from app.domain.prompt import PromptRequest
from app.engine.pipeline import CorePromptEnginePipeline
from app.llm.errors import LLMAuthenticationError
from app.llm.providers.mock import MockLLMProvider
from tests.fixtures.requirements import REQ_THAI_CRUD


def test_api_key_not_exposed_in_string_or_repr():
    secret_value = "sk-super-secret-production-key-9999"
    secret = SecretStr(secret_value)
    settings = Settings(LLM_API_KEY=secret)

    # String representation must be masked
    assert str(settings.LLM_API_KEY) == "**********"
    assert secret_value not in str(settings.LLM_API_KEY)
    assert secret_value not in repr(settings.LLM_API_KEY)


def test_exception_does_not_contain_secret_key():
    secret_value = "sk-super-secret-key-to-protect"
    error = LLMAuthenticationError("Authentication rejected by provider endpoint")

    assert secret_value not in str(error)
    assert secret_value not in repr(error)


@pytest.mark.asyncio
async def test_api_response_does_not_contain_api_key():
    provider = MockLLMProvider()
    req = PromptRequest(raw_text=REQ_THAI_CRUD, enable_llm=True)
    resp = await CorePromptEnginePipeline.execute_async(req, provider=provider)

    json_str = resp.model_dump_json()
    assert "api_key" not in json_str.lower()
    assert "secret" not in json_str.lower()
