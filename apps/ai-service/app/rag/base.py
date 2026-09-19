from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseKnowledgeRetriever(ABC):
    """
    Abstract interface for knowledge retrieval (RAG).
    In M1, serves as an architectural boundary.
    Concrete vector storage (Qdrant) will be introduced in Milestone 5 (Knowledge / RAG).
    """

    @abstractmethod
    async def retrieve(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Retrieve relevant context snippets for a query."""
        pass
