import asyncio
import logging
from typing import Any, Optional
from datetime import datetime, timedelta
from src.domain.interfaces.cache import ICache

logger = logging.getLogger(__name__)


class MemoryCache(ICache):
    """Implementação de cache em memória."""

    def __init__(self):
        self.cache: dict[str, tuple[Any, datetime]] = {}
        self.lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[Any]:
        """Obtém um valor do cache."""
        async with self.lock:
            if key not in self.cache:
                return None

            value, expiration = self.cache[key]
            if datetime.now() > expiration:
                del self.cache[key]
                return None

            return value

    async def set(self, key: str, value: Any, ttl: int) -> None:
        """Define um valor no cache com TTL."""
        async with self.lock:
            expiration = datetime.now() + timedelta(seconds=ttl)
            self.cache[key] = (value, expiration)
            logger.debug(f"Cache set: {key} (TTL: {ttl}s)")

    async def delete(self, key: str) -> None:
        """Deleta um valor do cache."""
        async with self.lock:
            if key in self.cache:
                del self.cache[key]
                logger.debug(f"Cache deleted: {key}")

    async def clear(self) -> None:
        """Limpa todo o cache."""
        async with self.lock:
            self.cache.clear()
            logger.debug("Cache cleared")

    async def exists(self, key: str) -> bool:
        """Verifica se uma chave existe no cache."""
        async with self.lock:
            if key not in self.cache:
                return False

            value, expiration = self.cache[key]
            if datetime.now() > expiration:
                del self.cache[key]
                return False

            return True
