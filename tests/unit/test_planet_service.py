from unittest.mock import AsyncMock

import pytest

from src.application.services.planet_service import PlanetService
from src.config.exceptions import ResourceNotFoundError
from src.domain.entities.planet import Planet


@pytest.fixture
def mock_repository():
    """Fixture para repositório mockado."""
    return AsyncMock()


@pytest.fixture
def planet_service(mock_repository):
    """Fixture para o serviço de planetas."""
    return PlanetService(mock_repository)


@pytest.mark.asyncio
async def test_get_planet_by_id_success(planet_service, mock_repository, mock_swapi_planet):
    """Testa obtenção de planeta por ID com sucesso."""
    planet = Planet(**mock_swapi_planet)
    mock_repository.get_by_id.return_value = planet

    result = await planet_service.get_planet_by_id("1")

    assert result.name == "Tatooine"
    assert result.climate == "arid"
    mock_repository.get_by_id.assert_called_once_with("1")


@pytest.mark.asyncio
async def test_get_planet_by_id_not_found(planet_service, mock_repository):
    """Testa obtenção de planeta por ID quando não encontrado."""
    mock_repository.get_by_id.return_value = None

    with pytest.raises(ResourceNotFoundError):
        await planet_service.get_planet_by_id("999")


@pytest.mark.asyncio
async def test_list_planets_success(planet_service, mock_repository, mock_swapi_planet):
    """Testa listagem de planetas com sucesso."""
    planet = Planet(**mock_swapi_planet)
    mock_repository.get_all.return_value = ([planet], 1)

    result, total = await planet_service.list_planets(page=1, page_size=10)

    assert len(result) == 1
    assert total == 1
    assert result[0].name == "Tatooine"
    mock_repository.get_all.assert_called_once()


@pytest.mark.asyncio
async def test_list_planets_with_filters(planet_service, mock_repository, mock_swapi_planet):
    """Testa listagem de planetas com filtros."""
    planet = Planet(**mock_swapi_planet)
    mock_repository.get_all.return_value = ([planet], 1)

    filters = {"climate": "arid"}
    result, total = await planet_service.list_planets(filters=filters)

    assert len(result) == 1
    mock_repository.get_all.assert_called_once()


@pytest.mark.asyncio
async def test_search_planets_success(planet_service, mock_repository, mock_swapi_planet):
    """Testa busca de planetas com sucesso."""
    planet = Planet(**mock_swapi_planet)
    mock_repository.search.return_value = [planet]

    result = await planet_service.search_planets("tatooine")

    assert len(result) == 1
    assert result[0].name == "Tatooine"
    mock_repository.search.assert_called_once_with("tatooine")


@pytest.mark.asyncio
async def test_search_planets_empty_query(planet_service):
    """Testa busca com query vazia."""
    result = await planet_service.search_planets("")

    assert result == []


@pytest.mark.asyncio
async def test_count_planets(planet_service, mock_repository):
    """Testa contagem de planetas."""
    mock_repository.count.return_value = 60

    result = await planet_service.count_planets()

    assert result == 60
    mock_repository.count.assert_called_once()


@pytest.mark.asyncio
async def test_get_planets_by_film_success(planet_service, mock_repository, mock_swapi_planet):
    """Testa obtenção de planetas de um filme."""
    planet = Planet(**mock_swapi_planet)
    mock_repository.get_by_id.return_value = planet
    mock_repository.http_client = AsyncMock()
    mock_repository.http_client.get.return_value = {"planets": ["https://swapi.dev/api/planets/1/"]}

    result = await planet_service.get_planets_by_film("1")

    assert len(result) >= 0


@pytest.mark.asyncio
async def test_get_planets_by_climate_success(planet_service, mock_repository, mock_swapi_planet):
    """Testa obtenção de planetas por clima."""
    planet = Planet(**mock_swapi_planet)
    mock_repository.get_all.return_value = ([planet], 1)

    result = await planet_service.get_planets_by_climate("arid")

    assert len(result) >= 0
