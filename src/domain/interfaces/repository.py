from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, TypeVar

T = TypeVar("T")


class IRepository(ABC, Generic[T]):
    """Interface base para repositórios."""

    @abstractmethod
    async def get_by_id(self, resource_id: str) -> Optional[T]:
        """Obtém um recurso pelo ID."""
        pass

    @abstractmethod
    async def get_all(
        self,
        page: int = 1,
        page_size: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        sort_by: Optional[str] = None,
        sort_order: str = "asc",
    ) -> tuple[List[T], int]:
        """Obtém todos os recursos com paginação, filtros e ordenação."""
        pass

    @abstractmethod
    async def search(self, query: str) -> List[T]:
        """Busca recursos por query."""
        pass

    @abstractmethod
    async def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Conta o número de recursos."""
        pass
