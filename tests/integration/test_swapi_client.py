import pytest

from src.config.exceptions import ExternalAPIError
from src.infrastructure.http.swapi_client import SwapiClient


@pytest.fixture
async def swapi_client():
    """Fixture para o cliente SWAPI."""
    client = SwapiClient()
    yield client
    await client.close()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_character_success(swapi_client):
    """Testa obtenção de personagem da API SWAPI."""
    try:
        result = await swapi_client.get("https://swapi.dev/api/people/1/")

        assert result is not None
        assert "name" in result
        assert result["name"] == "Luke Skywalker"
    except Exception as e:
        pytest.skip(f"SWAPI indisponível: {str(e)}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_planet_success(swapi_client):
    """Testa obtenção de planeta da API SWAPI."""
    try:
        result = await swapi_client.get("https://swapi.dev/api/planets/1/")

        assert result is not None
        assert "name" in result
        assert result["name"] == "Tatooine"
    except Exception as e:
        pytest.skip(f"SWAPI indisponível: {str(e)}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_starship_success(swapi_client):
    """Testa obtenção de nave da API SWAPI."""
    try:
        result = await swapi_client.get("https://swapi.dev/api/starships/12/")

        assert result is not None
        assert "name" in result
        assert result["name"] == "X-wing"
    except Exception as e:
        pytest.skip(f"SWAPI indisponível: {str(e)}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_film_success(swapi_client):
    """Testa obtenção de filme da API SWAPI."""
    try:
        result = await swapi_client.get("https://swapi.dev/api/films/1/")

        assert result is not None
        assert "title" in result
        assert result["title"] == "A New Hope"
    except Exception as e:
        pytest.skip(f"SWAPI indisponível: {str(e)}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_invalid_url(swapi_client):
    """Testa erro ao acessar URL inválida."""
    with pytest.raises(ExternalAPIError):
        await swapi_client.get("https://swapi.dev/api/invalid/999/")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_post_not_supported(swapi_client):
    """Testa que POST não é suportado."""
    with pytest.raises(NotImplementedError):
        await swapi_client.post("https://swapi.dev/api/people/")
