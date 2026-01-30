import httpx
import logging
from typing import Any, Dict, Optional
from src.domain.interfaces.client import IHttpClient
from src.config.settings import settings
from src.config.exceptions import ExternalAPIError

logger = logging.getLogger(__name__)


class SwapiClient(IHttpClient):
    """Cliente HTTP para a API SWAPI."""

    def __init__(self, base_url: str = settings.SWAPI_BASE_URL, timeout: int = settings.SWAPI_TIMEOUT):
        self.base_url = base_url
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout)

    async def get(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Faz uma requisição GET para SWAPI."""
        try:
            timeout = timeout or self.timeout
            response = await self.client.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"Erro HTTP ao acessar {url}: {e.response.status_code}")
            raise ExternalAPIError(
                f"Erro ao acessar SWAPI: {e.response.status_code}",
                status_code=e.response.status_code,
            )
        except httpx.TimeoutException:
            logger.error(f"Timeout ao acessar {url}")
            raise ExternalAPIError("Timeout ao acessar SWAPI", status_code=504)
        except httpx.RequestError as e:
            logger.error(f"Erro de requisição ao acessar {url}: {str(e)}")
            raise ExternalAPIError(f"Erro ao acessar SWAPI: {str(e)}", status_code=502)
        except Exception as e:
            logger.error(f"Erro inesperado ao acessar {url}: {str(e)}")
            raise ExternalAPIError(f"Erro inesperado ao acessar SWAPI: {str(e)}")

    async def post(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Faz uma requisição POST para SWAPI (não suportado)."""
        raise NotImplementedError("SWAPI não suporta requisições POST")

    async def close(self) -> None:
        """Fecha a conexão do cliente."""
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
