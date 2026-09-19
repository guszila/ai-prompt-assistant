from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class RequirementLanguage(str, Enum):
    THAI = "th"
    ENGLISH = "en"


class PromptStatus(str, Enum):
    DRAFT = "draft"
    ANALYZED = "analyzed"
    GENERATED = "generated"
    REVIEWED = "reviewed"
    APPROVED = "approved"
    REJECTED = "rejected"


class PromptRequest(BaseModel):
    """Lightweight contract for incoming user requirement."""
    id: str
    raw_text: str = Field(..., min_length=1)
    language: RequirementLanguage = RequirementLanguage.THAI
    project_context_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PromptAnalysis(BaseModel):
    """Lightweight contract for requirement analysis."""
    request_id: str
    identified_intent: str
    technical_domain: str
    ambiguities: List[str] = Field(default_factory=list)
    extracted_constraints: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    suggested_clarifications: List[str] = Field(default_factory=list)


class EngineeringPrompt(BaseModel):
    """Lightweight contract for structured prompt."""
    id: str
    request_id: str
    title: str
    system_context: str
    role_definition: str
    task_instructions: str
    technical_constraints: List[str] = Field(default_factory=list)
    input_output_specification: str
    verification_steps: List[str] = Field(default_factory=list)
    version: int = 1
    status: PromptStatus = PromptStatus.GENERATED
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PromptFeedback(BaseModel):
    """Lightweight contract for user feedback."""
    id: str
    prompt_id: str
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    user_comment: Optional[str] = None
    revised_prompt_content: Optional[str] = None
    is_accepted: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
