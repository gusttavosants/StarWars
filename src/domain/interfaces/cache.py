from abc import ABC, abstractmethod
from typing import Any, Optional


class ICache(ABC):
    """Interface para cache."""

    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """Obtém um valor do cache."""
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, ttl: int) -> None:
        """Define um valor no cache com TTL."""
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        """Deleta um valor do cache."""
        pass

    @abstractmethod
    async def clear(self) -> None:
        """Limpa todo o cache."""
        pass

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """Verifica se uma chave existe no cache."""
        pass
