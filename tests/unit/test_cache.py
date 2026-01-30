import pytest

from src.infrastructure.cache.memory_cache import MemoryCache


@pytest.fixture
def memory_cache():
    """Fixture para cache em memória."""
    return MemoryCache()


@pytest.mark.asyncio
async def test_set_and_get(memory_cache):
    """Testa set e get no cache."""
    await memory_cache.set("key1", {"data": "value"}, 3600)
    result = await memory_cache.get("key1")

    assert result is not None
    assert result["data"] == "value"


@pytest.mark.asyncio
async def test_get_nonexistent_key(memory_cache):
    """Testa get de chave inexistente."""
    result = await memory_cache.get("nonexistent")

    assert result is None


@pytest.mark.asyncio
async def test_delete(memory_cache):
    """Testa delete no cache."""
    await memory_cache.set("key1", {"data": "value"}, 3600)
    await memory_cache.delete("key1")
    result = await memory_cache.get("key1")

    assert result is None


@pytest.mark.asyncio
async def test_exists(memory_cache):
    """Testa exists no cache."""
    await memory_cache.set("key1", {"data": "value"}, 3600)

    assert await memory_cache.exists("key1") is True
    assert await memory_cache.exists("nonexistent") is False


@pytest.mark.asyncio
async def test_clear(memory_cache):
    """Testa clear no cache."""
    await memory_cache.set("key1", {"data": "value1"}, 3600)
    await memory_cache.set("key2", {"data": "value2"}, 3600)

    await memory_cache.clear()

    assert await memory_cache.get("key1") is None
    assert await memory_cache.get("key2") is None


@pytest.mark.asyncio
async def test_ttl_expiration(memory_cache):
    """Testa expiração de TTL."""
    import asyncio

    await memory_cache.set("key1", {"data": "value"}, 1)

    assert await memory_cache.get("key1") is not None

    await asyncio.sleep(1.1)

    assert await memory_cache.get("key1") is None
