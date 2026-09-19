from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel, Field


class ProjectContext(BaseModel):
    """Lightweight contract for project-level conventions and guidelines."""
    id: str
    name: str
    tech_stack: List[str] = Field(default_factory=list)
    coding_rules: List[str] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Conversation(BaseModel):
    """Lightweight contract for interactive conversation sessions."""
    id: str
    title: str
    project_context_id: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
