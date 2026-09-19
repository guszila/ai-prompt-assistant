import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from app.llm.models import LLMMetadata


class RequirementLanguage(str, Enum):
    THAI = "th"
    ENGLISH = "en"
    MIXED = "mixed"


class PromptStatus(str, Enum):
    DRAFT = "draft"
    ANALYZED = "analyzed"
    GENERATED = "generated"
    REVIEWED = "reviewed"
    APPROVED = "approved"
    REJECTED = "rejected"


class AmbiguitySeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Ambiguity(BaseModel):
    """Structured representation of missing or unclear requirement information."""
    ambiguity_id: str
    description: str
    severity: AmbiguitySeverity = AmbiguitySeverity.MEDIUM
    related_requirement: str = ""
    clarification_question: str
    is_functional: bool = True  # True if directly affects system functionality


class Assumption(BaseModel):
    """Explicitly captured inference derived from user wording."""
    assumption_id: str
    description: str
    source_concept: str
    requires_confirmation: bool = True


class TechnicalConcept(BaseModel):
    """Identified software engineering concept."""
    name: str
    category: str  # e.g., 'security', 'architecture', 'data', 'ui', 'operations'
    confidence: float = 1.0
    source_terms: List[str] = Field(default_factory=list)
    is_inferred: bool = False  # False = explicitly requested, True = derived inference


class NormalizedRequirement(BaseModel):
    """Normalized representation of user input while preserving the exact original."""
    original_text: str
    normalized_text: str
    detected_language: RequirementLanguage
    char_count: int
    word_count: int


class PromptRequest(BaseModel):
    """Incoming user requirement request."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    raw_text: str = Field(..., min_length=1)
    language: RequirementLanguage = RequirementLanguage.THAI
    project_context_id: Optional[str] = None
    enable_llm: Optional[bool] = None  # None uses server configuration default
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class RequirementAnalysis(BaseModel):
    """Structured analysis of user requirement without requirement fabrication."""
    request_id: str
    original_requirement: str
    normalized_requirement: str
    intent: str
    requested_actions: List[str] = Field(default_factory=list)
    entities: List[str] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)  # Explicit constraints only
    technical_concepts: List[TechnicalConcept] = Field(default_factory=list)
    expected_output: Optional[str] = None
    ambiguities: List[Ambiguity] = Field(default_factory=list)
    assumptions: List[Assumption] = Field(default_factory=list)


# Backward-compatible alias / adapter for M1 PromptAnalysis
class PromptAnalysis(BaseModel):
    """Backward-compatible contract for M1 PromptAnalysis."""
    request_id: str
    identified_intent: str
    technical_domain: str
    ambiguities: List[str] = Field(default_factory=list)
    extracted_constraints: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    suggested_clarifications: List[str] = Field(default_factory=list)


class EngineeringPrompt(BaseModel):
    """Structured engineering prompt formatted for AI coding agents."""
    id: str
    request_id: str
    title: str
    role: str = "Senior Software Engineer"
    objective: str
    context: str = ""
    requirements: List[str] = Field(default_factory=list)
    technical_details: List[str] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)
    expected_output: str = ""
    acceptance_criteria: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    clarification_questions: List[str] = Field(default_factory=list)
    raw_markdown: str = ""
    version: int = 1
    status: PromptStatus = PromptStatus.GENERATED
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Backward compatibility properties for M1 fields
    @property
    def system_context(self) -> str:
        return self.context

    @property
    def role_definition(self) -> str:
        return self.role

    @property
    def task_instructions(self) -> str:
        return "\n".join(self.requirements)

    @property
    def technical_constraints(self) -> List[str]:
        return self.constraints

    @property
    def input_output_specification(self) -> str:
        return self.expected_output

    @property
    def verification_steps(self) -> List[str]:
        return self.acceptance_criteria


class PromptFeedback(BaseModel):
    """User feedback for prompt evaluation."""
    id: str
    prompt_id: str
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    user_comment: Optional[str] = None
    revised_prompt_content: Optional[str] = None
    is_accepted: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PromptValidationResult(BaseModel):
    """Validation report for structured prompt and analysis."""
    is_valid: bool
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    validated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PromptTransformationResponse(BaseModel):
    """Complete aggregated response for prompt analysis and generation."""
    request_id: str
    normalized: NormalizedRequirement
    analysis: RequirementAnalysis
    prompt: EngineeringPrompt
    validation: PromptValidationResult
    llm_metadata: Optional[LLMMetadata] = None
