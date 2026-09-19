from pydantic import SecretStr
from app.core.config import Settings


def test_settings_default_llm_values():
    settings = Settings()
    assert settings.LLM_PROVIDER in ["mock", "openai"]
    assert settings.LLM_MODEL != ""
    assert settings.LLM_TIMEOUT_SECONDS > 0
    assert settings.LLM_MAX_RETRIES >= 0


def test_secret_str_masks_api_key():
    secret_key = "sk-test-secret-key-1234567890"
    settings = Settings(LLM_API_KEY=secret_key)

    assert settings.LLM_API_KEY is not None
    assert isinstance(settings.LLM_API_KEY, SecretStr)

    # String and repr representations must be masked
    assert str(settings.LLM_API_KEY) == "**********"
    assert secret_key not in str(settings.LLM_API_KEY)
    assert secret_key not in repr(settings.LLM_API_KEY)

    # Access is only available via get_secret_value()
    assert settings.LLM_API_KEY.get_secret_value() == secret_key
