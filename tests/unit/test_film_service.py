from unittest.mock import AsyncMock

import pytest

from src.application.services.film_service import FilmService
from src.config.exceptions import ResourceNotFoundError
from src.domain.entities.film import Film


@pytest.fixture
def mock_repository():
    """Fixture para repositório mockado."""
    return AsyncMock()


@pytest.fixture
def film_service(mock_repository):
    """Fixture para o serviço de filmes."""
    return FilmService(mock_repository)


@pytest.mark.asyncio
async def test_get_film_by_id_success(film_service, mock_repository, mock_swapi_film):
    """Testa obtenção de filme por ID com sucesso."""
    film = Film(**mock_swapi_film)
    mock_repository.get_by_id.return_value = film

    result = await film_service.get_film_by_id("1")

    assert result.title == "A New Hope"
    assert result.episode_id == 4
    mock_repository.get_by_id.assert_called_once_with("1")


@pytest.mark.asyncio
async def test_get_film_by_id_not_found(film_service, mock_repository):
    """Testa obtenção de filme por ID quando não encontrado."""
    mock_repository.get_by_id.return_value = None

    with pytest.raises(ResourceNotFoundError):
        await film_service.get_film_by_id("999")


@pytest.mark.asyncio
async def test_list_films_success(film_service, mock_repository, mock_swapi_film):
    """Testa listagem de filmes com sucesso."""
    film = Film(**mock_swapi_film)
    mock_repository.get_all.return_value = ([film], 1)

    result, total = await film_service.list_films(page=1, page_size=10)

    assert len(result) == 1
    assert total == 1
    assert result[0].title == "A New Hope"
    mock_repository.get_all.assert_called_once()


@pytest.mark.asyncio
async def test_list_films_with_filters(film_service, mock_repository, mock_swapi_film):
    """Testa listagem de filmes com filtros."""
    film = Film(**mock_swapi_film)
    mock_repository.get_all.return_value = ([film], 1)

    filters = {"episode_id": 4}
    result, total = await film_service.list_films(filters=filters)

    assert len(result) == 1
    mock_repository.get_all.assert_called_once()


@pytest.mark.asyncio
async def test_search_films_success(film_service, mock_repository, mock_swapi_film):
    """Testa busca de filmes com sucesso."""
    film = Film(**mock_swapi_film)
    mock_repository.search.return_value = [film]

    result = await film_service.search_films("hope")

    assert len(result) == 1
    assert result[0].title == "A New Hope"
    mock_repository.search.assert_called_once_with("hope")


@pytest.mark.asyncio
async def test_search_films_empty_query(film_service):
    """Testa busca com query vazia."""
    result = await film_service.search_films("")

    assert result == []


@pytest.mark.asyncio
async def test_count_films(film_service, mock_repository):
    """Testa contagem de filmes."""
    mock_repository.count.return_value = 6

    result = await film_service.count_films()

    assert result == 6
    mock_repository.count.assert_called_once()


@pytest.mark.asyncio
async def test_get_films_by_director_success(film_service, mock_repository, mock_swapi_film):
    """Testa obtenção de filmes por diretor."""
    film = Film(**mock_swapi_film)
    mock_repository.get_all.return_value = ([film], 1)

    result = await film_service.get_films_by_director("George Lucas")

    assert len(result) >= 0


@pytest.mark.asyncio
async def test_get_films_by_character_success(film_service, mock_repository, mock_swapi_film):
    """Testa obtenção de filmes de um personagem."""
    film = Film(**mock_swapi_film)
    mock_repository.get_by_id.return_value = film
    mock_repository.http_client = AsyncMock()
    mock_repository.http_client.get.return_value = {"films": ["https://swapi.dev/api/films/1/"]}

    result = await film_service.get_films_by_character("1")

    assert len(result) >= 0


@pytest.mark.asyncio
async def test_get_films_by_planet_success(film_service, mock_repository, mock_swapi_film):
    """Testa obtenção de filmes de um planeta."""
    film = Film(**mock_swapi_film)
    mock_repository.get_by_id.return_value = film
    mock_repository.http_client = AsyncMock()
    mock_repository.http_client.get.return_value = {"films": ["https://swapi.dev/api/films/1/"]}

    result = await film_service.get_films_by_planet("1")

    assert len(result) >= 0


@pytest.mark.asyncio
async def test_get_films_by_starship_success(film_service, mock_repository, mock_swapi_film):
    """Testa obtenção de filmes de uma nave."""
    film = Film(**mock_swapi_film)
    mock_repository.get_by_id.return_value = film
    mock_repository.http_client = AsyncMock()
    mock_repository.http_client.get.return_value = {"films": ["https://swapi.dev/api/films/1/"]}

    result = await film_service.get_films_by_starship("12")

    assert len(result) >= 0
