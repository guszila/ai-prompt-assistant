from app.llm.models import LLMFallbackReason


class LLMError(Exception):
    """Base exception for all LLM subsystem errors."""
    def __init__(self, message: str, reason: LLMFallbackReason):
        super().__init__(message)
        self.message = message
        self.reason = reason


class LLMConfigurationError(LLMError):
    """Missing API key or invalid provider configuration (non-retryable)."""
    def __init__(self, message: str = "Invalid or missing LLM configuration"):
        super().__init__(message, LLMFallbackReason.CONFIGURATION_ERROR)


class LLMAuthenticationError(LLMError):
    """Authentication or authorization failure with provider (non-retryable)."""
    def __init__(self, message: str = "Provider authentication failed"):
        super().__init__(message, LLMFallbackReason.AUTHENTICATION_ERROR)


class LLMTimeoutError(LLMError):
    """Request exceeded configured timeout window (retryable)."""
    def __init__(self, message: str = "Provider request timed out"):
        super().__init__(message, LLMFallbackReason.TIMEOUT)


class LLMRateLimitError(LLMError):
    """Provider rate limit or quota exceeded (retryable with backoff)."""
    def __init__(self, message: str = "Provider rate limit exceeded"):
        super().__init__(message, LLMFallbackReason.RATE_LIMIT)


class LLMNetworkError(LLMError):
    """Connection, DNS, or socket failure (retryable)."""
    def __init__(self, message: str = "Network connection to provider failed"):
        super().__init__(message, LLMFallbackReason.NETWORK_ERROR)


class LLMValidationError(LLMError):
    """Model output failed schema validation or could not be parsed into candidate model."""
    def __init__(self, message: str = "Model output failed schema validation"):
        super().__init__(message, LLMFallbackReason.VALIDATION_ERROR)
