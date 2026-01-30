import logging
from src.domain.interfaces.cache import ICache
from src.infrastructure.cache.memory_cache import MemoryCache
from src.infrastructure.cache.redis_cache import RedisCache
from src.config.settings import settings

logger = logging.getLogger(__name__)


class CacheFactory:
    """Factory para criar instâncias de cache."""

    @staticmethod
    def create_cache() -> ICache:
        """Cria uma instância de cache baseada na configuração."""
        if settings.REDIS_URL:
            logger.info("Usando Redis como cache")
            return RedisCache(settings.REDIS_URL)
        else:
            logger.info("Usando cache em memória")
            return MemoryCache()
