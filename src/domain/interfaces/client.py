from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class IHttpClient(ABC):
    """Interface para cliente HTTP."""

    @abstractmethod
    async def get(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Faz uma requisição GET."""
        pass

    @abstractmethod
    async def post(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Faz uma requisição POST."""
        pass

    @abstractmethod
    async def close(self) -> None:
        """Fecha a conexão do cliente."""
        pass
