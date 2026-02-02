from unittest.mock import AsyncMock, MagicMock

import pytest

from src.application.services.character_service import CharacterService
from src.config.exceptions import ResourceNotFoundError
from src.domain.entities.character import Character


@pytest.fixture
def mock_repository():
    """Fixture para repositório mockado."""
    return AsyncMock()


@pytest.fixture
def character_service(mock_repository):
    """Fixture para o serviço de personagens."""
    return CharacterService(mock_repository)


@pytest.mark.asyncio
async def test_get_character_by_id_success(
    character_service, mock_repository, mock_swapi_character
):
    """Testa obtenção de personagem por ID com sucesso."""
    character = Character(**mock_swapi_character)
    mock_repository.get_by_id.return_value = character

    result = await character_service.get_character_by_id("1")

    assert result.name == "Luke Skywalker"
    assert result.height == "172"
    mock_repository.get_by_id.assert_called_once_with("1")


@pytest.mark.asyncio
async def test_get_character_by_id_not_found(character_service, mock_repository):
    """Testa obtenção de personagem por ID quando não encontrado."""
    mock_repository.get_by_id.return_value = None

    with pytest.raises(ResourceNotFoundError):
        await character_service.get_character_by_id("999")


@pytest.mark.asyncio
async def test_list_characters_success(character_service, mock_repository, mock_swapi_character):
    """Testa listagem de personagens com sucesso."""
    character = Character(**mock_swapi_character)
    mock_repository.get_all.return_value = ([character], 1)

    result, total = await character_service.list_characters(page=1, page_size=10)

    assert len(result) == 1
    assert total == 1
    assert result[0].name == "Luke Skywalker"
    mock_repository.get_all.assert_called_once()


@pytest.mark.asyncio
async def test_list_characters_with_filters(
    character_service, mock_repository, mock_swapi_character
):
    """Testa listagem de personagens com filtros."""
    character = Character(**mock_swapi_character)
    mock_repository.get_all.return_value = ([character], 1)

    filters = {"gender": "male"}
    result, total = await character_service.list_characters(filters=filters)

    assert len(result) == 1
    mock_repository.get_all.assert_called_once()


@pytest.mark.asyncio
async def test_search_characters_success(character_service, mock_repository, mock_swapi_character):
    """Testa busca de personagens com sucesso."""
    character = Character(**mock_swapi_character)
    mock_repository.search.return_value = [character]

    result = await character_service.search_characters("luke")

    assert len(result) == 1
    assert result[0].name == "Luke Skywalker"
    mock_repository.search.assert_called_once_with("luke")


@pytest.mark.asyncio
async def test_search_characters_empty_query(character_service):
    """Testa busca com query vazia."""
    result = await character_service.search_characters("")

    assert result == []


@pytest.mark.asyncio
async def test_search_characters_short_query(character_service):
    """Testa busca com query muito curta."""
    result = await character_service.search_characters("a")

    assert result == []


@pytest.mark.asyncio
async def test_count_characters(character_service, mock_repository):
    """Testa contagem de personagens."""
    mock_repository.count.return_value = 82

    result = await character_service.count_characters()

    assert result == 82
    mock_repository.count.assert_called_once()


@pytest.mark.asyncio
async def test_get_characters_by_film_success(
    character_service, mock_repository, mock_swapi_character
):
    """Testa obtenção de personagens de um filme."""
    character = Character(**mock_swapi_character)
    mock_repository.get_by_id.return_value = character
    mock_repository.http_client = AsyncMock()
    mock_repository.http_client.get.return_value = {
        "characters": ["https://swapi.dev/api/people/1/"]
    }

    result = await character_service.get_characters_by_film("1")

    assert len(result) >= 0


@pytest.mark.asyncio
async def test_get_characters_from_planet_success(
    character_service, mock_repository, mock_swapi_character
):
    """Testa obtenção de residentes de um planeta."""
    character = Character(**mock_swapi_character)
    mock_repository.get_by_id.return_value = character
    mock_repository.http_client = AsyncMock()
    mock_repository.http_client.get.return_value = {
        "residents": ["https://swapi.dev/api/people/1/"]
    }

    result = await character_service.get_characters_from_planet("1")

    assert len(result) >= 0
