from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class LLMFallbackReason(str, Enum):
    """Specific failure reasons triggering fallback to M2 deterministic baseline."""
    CONFIGURATION_ERROR = "configuration_error"
    AUTHENTICATION_ERROR = "authentication_error"
    TIMEOUT = "timeout"
    RATE_LIMIT = "rate_limit"
    NETWORK_ERROR = "network_error"
    VALIDATION_ERROR = "validation_error"


class LLMUsage(BaseModel):
    """Token consumption metrics for an LLM call."""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class LLMMetadata(BaseModel):
    """
    Execution and provenance metadata for the LLM enhancement step.
    Strictly contains execution telemetry, never unverified business requirements.
    """
    provider: str
    model: str
    enhanced: bool = False
    fallback_used: bool = False
    fallback_reason: Optional[LLMFallbackReason] = None
    latency_ms: Optional[float] = None
    usage: Optional[LLMUsage] = None


class LLMRequirementCandidate(BaseModel):
    """
    Untrusted candidate output extracted from LLM structured response.
    Never directly becomes the authoritative RequirementAnalysis without passing GroundingReconciler.
    """
    suggested_intent: Optional[str] = None
    suggested_actions: List[str] = Field(default_factory=list)
    suggested_entities: List[str] = Field(default_factory=list)
    suggested_concepts: List[str] = Field(default_factory=list)
    suggested_assumptions: List[str] = Field(default_factory=list)
    suggested_clarifications: List[str] = Field(default_factory=list)
