from abc import ABC, abstractmethod
from typing import Any, Dict
from app.domain.prompt import EngineeringPrompt
from app.domain.learning import EvaluationResult


class BaseEvaluator(ABC):
    """
    Abstract interface for prompt quality and regression evaluation.
    """

    @abstractmethod
    async def evaluate(self, prompt: EngineeringPrompt, **kwargs: Any) -> EvaluationResult:
        """Evaluate prompt quality against defined criteria."""
        pass
