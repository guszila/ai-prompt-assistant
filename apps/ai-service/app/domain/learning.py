from datetime import datetime, timezone
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class Experience(BaseModel):
    """Lightweight contract for experience records saved for future curation."""
    id: str
    request_id: str
    prompt_id: str
    feedback_id: Optional[str] = None
    is_curated: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class EvaluationResult(BaseModel):
    """Lightweight contract for evaluation benchmark outputs."""
    id: str
    prompt_id: str
    metric_name: str
    score: float
    details: Dict[str, Any] = Field(default_factory=dict)
    evaluated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ModelVersion(BaseModel):
    """Lightweight contract for tracking model providers and identifiers."""
    id: str
    provider: str
    model_identifier: str
    is_local: bool = False
    active: bool = True
