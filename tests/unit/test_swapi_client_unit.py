from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from src.config.exceptions import ExternalAPIError
from src.infrastructure.http.swapi_client import SwapiClient


@pytest.fixture
async def swapi_client():
    """Fixture para cliente SWAPI."""
    client = SwapiClient()
    yield client
    await client.close()


@pytest.mark.asyncio
async def test_swapi_client_init(swapi_client):
    """Testa inicialização do cliente SWAPI."""
    assert swapi_client.base_url == "https://swapi.dev/api"
    assert swapi_client.timeout == 10
    assert swapi_client.client is not None


@pytest.mark.asyncio
async def test_get_success(swapi_client):
    """Testa requisição GET com sucesso."""
    with patch.object(swapi_client.client, "get") as mock_get:
        mock_response = MagicMock()
        mock_response.json = AsyncMock(return_value={"name": "Luke Skywalker"})
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        result = await swapi_client.get("https://swapi.dev/api/people/1/")

        assert result["name"] == "Luke Skywalker"
        mock_get.assert_called_once()


@pytest.mark.asyncio
async def test_get_with_headers(swapi_client):
    """Testa requisição GET com headers customizados."""
    with patch.object(swapi_client.client, "get") as mock_get:
        mock_response = MagicMock()
        mock_response.json = AsyncMock(return_value={"name": "Luke"})
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        headers = {"X-Custom": "value"}
        result = await swapi_client.get("https://swapi.dev/api/people/1/", headers=headers)

        assert result["name"] == "Luke"
        mock_get.assert_called_once()


@pytest.mark.asyncio
async def test_get_with_custom_timeout(swapi_client):
    """Testa requisição GET com timeout customizado."""
    with patch.object(swapi_client.client, "get") as mock_get:
        mock_response = MagicMock()
        mock_response.json = AsyncMock(return_value={"name": "Luke"})
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        result = await swapi_client.get("https://swapi.dev/api/people/1/", timeout=30)

        assert result["name"] == "Luke"


@pytest.mark.asyncio
async def test_get_timeout_error(swapi_client):
    """Testa requisição GET com timeout."""
    with patch.object(swapi_client.client, "get") as mock_get:
        mock_get.side_effect = httpx.TimeoutException("Timeout")

        with pytest.raises(ExternalAPIError):
            await swapi_client.get("https://swapi.dev/api/people/1/")


@pytest.mark.asyncio
async def test_get_request_error(swapi_client):
    """Testa requisição GET com erro de requisição."""
    with patch.object(swapi_client.client, "get") as mock_get:
        mock_get.side_effect = httpx.RequestError("Connection error")

        with pytest.raises(ExternalAPIError):
            await swapi_client.get("https://swapi.dev/api/people/1/")


@pytest.mark.asyncio
async def test_get_unexpected_error(swapi_client):
    """Testa requisição GET com erro inesperado."""
    with patch.object(swapi_client.client, "get") as mock_get:
        mock_get.side_effect = Exception("Unexpected error")

        with pytest.raises(ExternalAPIError):
            await swapi_client.get("https://swapi.dev/api/people/1/")


@pytest.mark.asyncio
async def test_post_not_implemented(swapi_client):
    """Testa que POST não é implementado."""
    with pytest.raises(NotImplementedError):
        await swapi_client.post("https://swapi.dev/api/people/")


@pytest.mark.asyncio
async def test_close(swapi_client):
    """Testa fechamento do cliente."""
    with patch.object(swapi_client.client, "aclose") as mock_close:
        await swapi_client.close()
        mock_close.assert_called_once()


@pytest.mark.asyncio
async def test_context_manager(swapi_client):
    """Testa uso como context manager."""
    async with swapi_client as client:
        assert client is not None


@pytest.mark.asyncio
async def test_get_json_parsing(swapi_client):
    """Testa parsing de JSON na resposta."""
    with patch.object(swapi_client.client, "get") as mock_get:
        mock_response = MagicMock()
        mock_response.json = AsyncMock(
            return_value={
                "name": "Luke Skywalker",
                "height": "172",
                "mass": "77",
                "hair_color": "blond",
            }
        )
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        result = await swapi_client.get("https://swapi.dev/api/people/1/")

        assert result["name"] == "Luke Skywalker"
        assert result["height"] == "172"
        assert result["mass"] == "77"
        assert result["hair_color"] == "blond"


@pytest.mark.asyncio
async def test_get_empty_response(swapi_client):
    """Testa resposta vazia."""
    with patch.object(swapi_client.client, "get") as mock_get:
        mock_response = MagicMock()
        mock_response.json = AsyncMock(return_value={})
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        result = await swapi_client.get("https://swapi.dev/api/people/1/")

        assert result == {}


@pytest.mark.asyncio
async def test_get_list_response(swapi_client):
    """Testa resposta com lista."""
    with patch.object(swapi_client.client, "get") as mock_get:
        mock_response = MagicMock()
        mock_response.json = AsyncMock(
            return_value={"count": 2, "results": [{"name": "Luke"}, {"name": "Yoda"}]}
        )
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        result = await swapi_client.get("https://swapi.dev/api/people/")

        assert result["count"] == 2
        assert len(result["results"]) == 2
