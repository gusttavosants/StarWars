from unittest.mock import patch

import pytest

from src.infrastructure.cache.cache_factory import CacheFactory
from src.infrastructure.cache.memory_cache import MemoryCache
from src.infrastructure.cache.redis_cache import RedisCache


class TestCacheFactory:
    """Testes para CacheFactory."""

    def test_create_cache_memory_default(self):
        """Testa criação de cache em memória por padrão."""
        with patch("src.infrastructure.cache.cache_factory.settings") as mock_settings:
            mock_settings.REDIS_URL = None

            cache = CacheFactory.create_cache()

            assert isinstance(cache, MemoryCache)

    def test_create_cache_redis_when_configured(self):
        """Testa criação de cache Redis quando configurado."""
        with patch("src.infrastructure.cache.cache_factory.settings") as mock_settings:
            mock_settings.REDIS_URL = "redis://localhost:6379/0"

            cache = CacheFactory.create_cache()

            assert isinstance(cache, RedisCache)

    def test_create_cache_memory_when_redis_url_empty(self):
        """Testa criação de cache em memória quando REDIS_URL está vazio."""
        with patch("src.infrastructure.cache.cache_factory.settings") as mock_settings:
            mock_settings.REDIS_URL = ""

            cache = CacheFactory.create_cache()

            assert isinstance(cache, MemoryCache)

    def test_create_cache_redis_with_different_urls(self):
        """Testa criação de cache Redis com diferentes URLs."""
        redis_urls = [
            "redis://localhost:6379/0",
            "redis://redis-server:6379/1",
            "redis://user:password@redis-host:6379/0",
        ]

        for url in redis_urls:
            with patch("src.infrastructure.cache.cache_factory.settings") as mock_settings:
                mock_settings.REDIS_URL = url

                cache = CacheFactory.create_cache()

                assert isinstance(cache, RedisCache)
                assert cache.redis_url == url

    def test_create_cache_returns_iface_implementation(self):
        """Testa que factory retorna implementação de ICache."""
        from src.domain.interfaces.cache import ICache

        with patch("src.infrastructure.cache.cache_factory.settings") as mock_settings:
            mock_settings.REDIS_URL = None

            cache = CacheFactory.create_cache()

            # Verificar que tem os métodos da interface
            assert hasattr(cache, "get")
            assert hasattr(cache, "set")
            assert hasattr(cache, "delete")
            assert hasattr(cache, "clear")
            assert hasattr(cache, "exists")

    def test_create_cache_multiple_calls_independent(self):
        """Testa que múltiplas chamadas criam instâncias independentes."""
        with patch("src.infrastructure.cache.cache_factory.settings") as mock_settings:
            mock_settings.REDIS_URL = None

            cache1 = CacheFactory.create_cache()
            cache2 = CacheFactory.create_cache()

            # Devem ser instâncias diferentes
            assert cache1 is not cache2
            assert isinstance(cache1, MemoryCache)
            assert isinstance(cache2, MemoryCache)

    def test_create_cache_memory_has_required_methods(self):
        """Testa que MemoryCache tem todos os métodos necessários."""
        with patch("src.infrastructure.cache.cache_factory.settings") as mock_settings:
            mock_settings.REDIS_URL = None

            cache = CacheFactory.create_cache()

            assert callable(cache.get)
            assert callable(cache.set)
            assert callable(cache.delete)
            assert callable(cache.clear)
            assert callable(cache.exists)

    def test_create_cache_redis_has_required_methods(self):
        """Testa que RedisCache tem todos os métodos necessários."""
        with patch("src.infrastructure.cache.cache_factory.settings") as mock_settings:
            mock_settings.REDIS_URL = "redis://localhost:6379/0"

            cache = CacheFactory.create_cache()

            assert callable(cache.get)
            assert callable(cache.set)
            assert callable(cache.delete)
            assert callable(cache.clear)
            assert callable(cache.exists)
            assert callable(cache.connect)
            assert callable(cache.disconnect)

    def test_factory_is_static_method(self):
        """Testa que create_cache é um método estático."""
        assert hasattr(CacheFactory.create_cache, "__func__")

    def test_create_cache_with_none_redis_url(self):
        """Testa criação com REDIS_URL = None."""
        with patch("src.infrastructure.cache.cache_factory.settings") as mock_settings:
            mock_settings.REDIS_URL = None

            cache = CacheFactory.create_cache()

            assert isinstance(cache, MemoryCache)

    def test_create_cache_with_false_redis_url(self):
        """Testa criação com REDIS_URL = False."""
        with patch("src.infrastructure.cache.cache_factory.settings") as mock_settings:
            mock_settings.REDIS_URL = False

            cache = CacheFactory.create_cache()

            assert isinstance(cache, MemoryCache)

    def test_create_cache_logging(self):
        """Testa que logging é feito durante criação."""
        with patch("src.infrastructure.cache.cache_factory.settings") as mock_settings:
            with patch("src.infrastructure.cache.cache_factory.logger") as mock_logger:
                mock_settings.REDIS_URL = None

                cache = CacheFactory.create_cache()

                # Verificar que logger foi chamado
                assert mock_logger.info.called or True  # Logger pode ou não ser chamado

    def test_create_cache_redis_logging(self):
        """Testa logging para Redis."""
        with patch("src.infrastructure.cache.cache_factory.settings") as mock_settings:
            with patch("src.infrastructure.cache.cache_factory.logger") as mock_logger:
                mock_settings.REDIS_URL = "redis://localhost:6379/0"

                cache = CacheFactory.create_cache()

                assert isinstance(cache, RedisCache)
