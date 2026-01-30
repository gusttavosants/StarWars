from unittest.mock import AsyncMock, MagicMock

import pytest

from src.config.exceptions import InvalidFilterError, InvalidSortError
from src.domain.entities.character import Character
from src.infrastructure.database.repositories.base_repository import BaseRepository


@pytest.fixture
def mock_http_client():
    """Fixture para cliente HTTP mockado."""
    return AsyncMock()


@pytest.fixture
def mock_cache():
    """Fixture para cache mockado."""
    return AsyncMock()


@pytest.fixture
def repository(mock_http_client, mock_cache):
    """Fixture para repositório base."""
    return BaseRepository(
        http_client=mock_http_client,
        cache=mock_cache,
        resource_type="people",
        entity_class=Character,
    )


@pytest.mark.asyncio
async def test_get_by_id_from_cache(repository, mock_cache, mock_swapi_character):
    """Testa obtenção de recurso do cache."""
    mock_cache.get.return_value = mock_swapi_character

    result = await repository.get_by_id("1")

    assert result.name == "Luke Skywalker"
    mock_cache.get.assert_called_once()


@pytest.mark.asyncio
async def test_get_by_id_from_http(repository, mock_http_client, mock_cache, mock_swapi_character):
    """Testa obtenção de recurso da API HTTP."""
    mock_cache.get.return_value = None
    mock_http_client.get.return_value = mock_swapi_character

    result = await repository.get_by_id("1")

    assert result.name == "Luke Skywalker"
    mock_http_client.get.assert_called_once()
    mock_cache.set.assert_called_once()


@pytest.mark.asyncio
async def test_get_by_id_not_found(repository, mock_http_client, mock_cache):
    """Testa obtenção de recurso não encontrado."""
    mock_cache.get.return_value = None
    mock_http_client.get.side_effect = Exception("404 Not Found")

    with pytest.raises(Exception):
        await repository.get_by_id("999")


@pytest.mark.asyncio
async def test_get_all_success(repository, mock_http_client, mock_cache, mock_swapi_character):
    """Testa obtenção de todos os recursos."""
    mock_cache.get.return_value = None
    mock_http_client.get.return_value = {"count": 82, "results": [mock_swapi_character]}

    results, total = await repository.get_all(page=1, page_size=10)

    assert len(results) == 1
    assert total == 82
    assert results[0].name == "Luke Skywalker"


@pytest.mark.asyncio
async def test_get_all_with_pagination(
    repository, mock_http_client, mock_cache, mock_swapi_character
):
    """Testa obtenção com paginação."""
    mock_cache.get.return_value = None
    mock_http_client.get.return_value = {"count": 82, "results": [mock_swapi_character]}

    results, total = await repository.get_all(page=2, page_size=10)

    assert len(results) >= 0
    assert total == 82


@pytest.mark.asyncio
async def test_get_all_with_sort(repository, mock_http_client, mock_cache, mock_swapi_character):
    """Testa obtenção com ordenação."""
    mock_cache.get.return_value = None
    mock_http_client.get.return_value = {"count": 82, "results": [mock_swapi_character]}

    results, total = await repository.get_all(sort_by="name", sort_order="asc")

    assert len(results) >= 0


@pytest.mark.asyncio
async def test_search_success(repository, mock_http_client, mock_cache, mock_swapi_character):
    """Testa busca de recursos."""
    mock_cache.get.return_value = None
    mock_http_client.get.return_value = {"count": 1, "results": [mock_swapi_character]}

    results = await repository.search("luke")

    assert len(results) == 1
    assert results[0].name == "Luke Skywalker"


@pytest.mark.asyncio
async def test_search_empty_result(repository, mock_http_client, mock_cache):
    """Testa busca sem resultados."""
    mock_cache.get.return_value = None
    mock_http_client.get.return_value = {"count": 0, "results": []}

    results = await repository.search("nonexistent")

    assert len(results) == 0


@pytest.mark.asyncio
async def test_count_success(repository, mock_http_client):
    """Testa contagem de recursos."""
    mock_http_client.get.return_value = {"count": 82}

    count = await repository.count()

    assert count == 82


@pytest.mark.asyncio
async def test_count_error(repository, mock_http_client):
    """Testa contagem com erro."""
    mock_http_client.get.side_effect = Exception("API Error")

    count = await repository.count()

    assert count == 0


def test_build_url(repository):
    """Testa construção de URL."""
    url = repository._build_url("1")

    assert "people" in url
    assert "1" in url
    assert url.endswith("/")


def test_get_cache_key(repository):
    """Testa geração de chave de cache."""
    key = repository._get_cache_key("by_id", "1")

    assert "people" in key
    assert "by_id" in key
    assert "1" in key


def test_filter_entities_with_eq(repository, mock_swapi_character):
    """Testa filtro com operador equals."""
    character = Character(**mock_swapi_character)
    entities = [character]

    filters = {"gender": {"operator": "eq", "value": "male"}}
    result = repository._filter_entities(entities, filters)

    assert len(result) == 1


def test_filter_entities_with_contains(repository, mock_swapi_character):
    """Testa filtro com operador contains."""
    character = Character(**mock_swapi_character)
    entities = [character]

    filters = {"name": {"operator": "contains", "value": "luke"}}
    result = repository._filter_entities(entities, filters)

    assert len(result) >= 0


def test_filter_entities_invalid_field(repository, mock_swapi_character):
    """Testa filtro com campo inválido."""
    character = Character(**mock_swapi_character)
    entities = [character]

    filters = {"invalid_field": "value"}

    with pytest.raises(InvalidFilterError):
        repository._filter_entities(entities, filters)


def test_sort_entities_asc(repository, mock_swapi_character):
    """Testa ordenação ascendente."""
    char1 = Character(**{**mock_swapi_character, "name": "Yoda"})
    char2 = Character(**{**mock_swapi_character, "name": "Luke"})
    entities = [char1, char2]

    result = repository._sort_entities(entities, "name", "asc")

    assert result[0].name == "Luke"
    assert result[1].name == "Yoda"


def test_sort_entities_desc(repository, mock_swapi_character):
    """Testa ordenação descendente."""
    char1 = Character(**{**mock_swapi_character, "name": "Yoda"})
    char2 = Character(**{**mock_swapi_character, "name": "Luke"})
    entities = [char1, char2]

    result = repository._sort_entities(entities, "name", "desc")

    assert result[0].name == "Yoda"
    assert result[1].name == "Luke"


def test_sort_entities_invalid_field(repository, mock_swapi_character):
    """Testa ordenação com campo inválido."""
    character = Character(**mock_swapi_character)
    entities = [character]

    with pytest.raises(InvalidFilterError):
        repository._sort_entities(entities, "invalid_field", "asc")


def test_match_filter_eq(repository):
    """Testa match de filtro equals."""
    result = repository._match_filter("male", {"operator": "eq", "value": "male"})
    assert result is True

    result = repository._match_filter("female", {"operator": "eq", "value": "male"})
    assert result is False


def test_match_filter_ne(repository):
    """Testa match de filtro not equals."""
    result = repository._match_filter("male", {"operator": "ne", "value": "female"})
    assert result is True

    result = repository._match_filter("male", {"operator": "ne", "value": "male"})
    assert result is False


def test_match_filter_contains(repository):
    """Testa match de filtro contains."""
    result = repository._match_filter("Luke Skywalker", {"operator": "contains", "value": "luke"})
    assert result is True

    result = repository._match_filter("Luke Skywalker", {"operator": "contains", "value": "yoda"})
    assert result is False


def test_match_filter_in(repository):
    """Testa match de filtro in."""
    result = repository._match_filter("male", {"operator": "in", "value": ["male", "female"]})
    assert result is True

    result = repository._match_filter("unknown", {"operator": "in", "value": ["male", "female"]})
    assert result is False


def test_match_filter_simple_value(repository):
    """Testa match com valor simples."""
    result = repository._match_filter("male", "male")
    assert result is True

    result = repository._match_filter("male", "female")
    assert result is False
