import redis.asyncio as redis
import logging
import json
from typing import Any, Optional
from src.domain.interfaces.cache import ICache
from src.config.exceptions import CacheError

logger = logging.getLogger(__name__)


class RedisCache(ICache):
    """Implementação de cache com Redis."""

    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.client: Optional[redis.Redis] = None

    async def connect(self) -> None:
        """Conecta ao Redis."""
        try:
            self.client = await redis.from_url(self.redis_url)
            await self.client.ping()
            logger.info("Conectado ao Redis com sucesso")
        except Exception as e:
            logger.error(f"Erro ao conectar ao Redis: {str(e)}")
            raise CacheError(f"Erro ao conectar ao Redis: {str(e)}")

    async def disconnect(self) -> None:
        """Desconecta do Redis."""
        if self.client:
            await self.client.close()
            logger.info("Desconectado do Redis")

    async def get(self, key: str) -> Optional[Any]:
        """Obtém um valor do cache."""
        if not self.client:
            raise CacheError("Cliente Redis não inicializado")

        try:
            value = await self.client.get(key)
            if value is None:
                return None
            return json.loads(value)
        except Exception as e:
            logger.error(f"Erro ao obter chave {key} do Redis: {str(e)}")
            return None

    async def set(self, key: str, value: Any, ttl: int) -> None:
        """Define um valor no cache com TTL."""
        if not self.client:
            raise CacheError("Cliente Redis não inicializado")

        try:
            await self.client.setex(key, ttl, json.dumps(value))
            logger.debug(f"Cache set: {key} (TTL: {ttl}s)")
        except Exception as e:
            logger.error(f"Erro ao definir chave {key} no Redis: {str(e)}")
            raise CacheError(f"Erro ao definir chave no Redis: {str(e)}")

    async def delete(self, key: str) -> None:
        """Deleta um valor do cache."""
        if not self.client:
            raise CacheError("Cliente Redis não inicializado")

        try:
            await self.client.delete(key)
            logger.debug(f"Cache deleted: {key}")
        except Exception as e:
            logger.error(f"Erro ao deletar chave {key} do Redis: {str(e)}")
            raise CacheError(f"Erro ao deletar chave do Redis: {str(e)}")

    async def clear(self) -> None:
        """Limpa todo o cache."""
        if not self.client:
            raise CacheError("Cliente Redis não inicializado")

        try:
            await self.client.flushdb()
            logger.debug("Cache cleared")
        except Exception as e:
            logger.error(f"Erro ao limpar Redis: {str(e)}")
            raise CacheError(f"Erro ao limpar Redis: {str(e)}")

    async def exists(self, key: str) -> bool:
        """Verifica se uma chave existe no cache."""
        if not self.client:
            raise CacheError("Cliente Redis não inicializado")

        try:
            return await self.client.exists(key) > 0
        except Exception as e:
            logger.error(f"Erro ao verificar existência da chave {key}: {str(e)}")
            return False
