from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")


class IRepository(ABC, Generic[T]):
    """
    Abstract repository interface.
    Ensures domain and application layers remain independent of persistence mechanisms.
    """

    @abstractmethod
    def get(self, entity_id: str) -> Optional[T]:
        """Fetch an entity by its identifier."""
        pass

    @abstractmethod
    def save(self, entity_id: str, data: T) -> None:
        """Create or update an entity."""
        pass

    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        """Delete an entity by its identifier. Returns True if deleted."""
        pass

    @abstractmethod
    def list_all(self) -> List[T]:
        """List all stored entities."""
        pass
