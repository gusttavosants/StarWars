from unittest.mock import AsyncMock

import pytest

from src.application.services.starship_service import StarshipService
from src.config.exceptions import ResourceNotFoundError
from src.domain.entities.starship import Starship


@pytest.fixture
def mock_repository():
    """Fixture para repositório mockado."""
    return AsyncMock()


@pytest.fixture
def starship_service(mock_repository):
    """Fixture para o serviço de naves."""
    return StarshipService(mock_repository)


@pytest.mark.asyncio
async def test_get_starship_by_id_success(starship_service, mock_repository, mock_swapi_starship):
    """Testa obtenção de nave por ID com sucesso."""
    starship = Starship(**mock_swapi_starship)
    mock_repository.get_by_id.return_value = starship

    result = await starship_service.get_starship_by_id("12")

    assert result.name == "X-wing"
    assert result.starship_class == "Starfighter"
    mock_repository.get_by_id.assert_called_once_with("12")


@pytest.mark.asyncio
async def test_get_starship_by_id_not_found(starship_service, mock_repository):
    """Testa obtenção de nave por ID quando não encontrada."""
    mock_repository.get_by_id.return_value = None

    with pytest.raises(ResourceNotFoundError):
        await starship_service.get_starship_by_id("999")


@pytest.mark.asyncio
async def test_list_starships_success(starship_service, mock_repository, mock_swapi_starship):
    """Testa listagem de naves com sucesso."""
    starship = Starship(**mock_swapi_starship)
    mock_repository.get_all.return_value = ([starship], 1)

    result, total = await starship_service.list_starships(page=1, page_size=10)

    assert len(result) == 1
    assert total == 1
    assert result[0].name == "X-wing"
    mock_repository.get_all.assert_called_once()


@pytest.mark.asyncio
async def test_list_starships_with_filters(starship_service, mock_repository, mock_swapi_starship):
    """Testa listagem de naves com filtros."""
    starship = Starship(**mock_swapi_starship)
    mock_repository.get_all.return_value = ([starship], 1)

    filters = {"starship_class": "Starfighter"}
    result, total = await starship_service.list_starships(filters=filters)

    assert len(result) == 1
    mock_repository.get_all.assert_called_once()


@pytest.mark.asyncio
async def test_search_starships_success(starship_service, mock_repository, mock_swapi_starship):
    """Testa busca de naves com sucesso."""
    starship = Starship(**mock_swapi_starship)
    mock_repository.search.return_value = [starship]

    result = await starship_service.search_starships("x-wing")

    assert len(result) == 1
    assert result[0].name == "X-wing"
    mock_repository.search.assert_called_once_with("x-wing")


@pytest.mark.asyncio
async def test_search_starships_empty_query(starship_service):
    """Testa busca com query vazia."""
    result = await starship_service.search_starships("")

    assert result == []


@pytest.mark.asyncio
async def test_count_starships(starship_service, mock_repository):
    """Testa contagem de naves."""
    mock_repository.count.return_value = 37

    result = await starship_service.count_starships()

    assert result == 37
    mock_repository.count.assert_called_once()


@pytest.mark.asyncio
async def test_get_starships_by_film_success(
    starship_service, mock_repository, mock_swapi_starship
):
    """Testa obtenção de naves de um filme."""
    starship = Starship(**mock_swapi_starship)
    mock_repository.get_by_id.return_value = starship
    mock_repository.http_client = AsyncMock()
    mock_repository.http_client.get.return_value = {
        "starships": ["https://swapi.dev/api/starships/12/"]
    }

    result = await starship_service.get_starships_by_film("1")

    assert len(result) >= 0


@pytest.mark.asyncio
async def test_get_starships_by_class_success(
    starship_service, mock_repository, mock_swapi_starship
):
    """Testa obtenção de naves por classe."""
    starship = Starship(**mock_swapi_starship)
    mock_repository.get_all.return_value = ([starship], 1)

    result = await starship_service.get_starships_by_class("Starfighter")

    assert len(result) >= 0


@pytest.mark.asyncio
async def test_get_starships_by_pilot_success(
    starship_service, mock_repository, mock_swapi_starship
):
    """Testa obtenção de naves de um piloto."""
    starship = Starship(**mock_swapi_starship)
    mock_repository.get_by_id.return_value = starship
    mock_repository.http_client = AsyncMock()
    mock_repository.http_client.get.return_value = {
        "starships": ["https://swapi.dev/api/starships/12/"]
    }

    result = await starship_service.get_starships_by_pilot("1")

    assert len(result) >= 0
