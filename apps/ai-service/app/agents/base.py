from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseAgent(ABC):
    """
    Abstract interface for specialized AI agents.
    Enforces clear inputs, outputs, and single responsibilities.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique agent identifier."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Description of the agent's responsibility."""
        pass

    @abstractmethod
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent task."""
        pass
