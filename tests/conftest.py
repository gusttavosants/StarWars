from unittest.mock import AsyncMock, Mock

import pytest

from src.config.settings import Settings


@pytest.fixture
def mock_settings():
    """Fixture para settings mockado."""
    settings = Mock(spec=Settings)
    settings.SWAPI_BASE_URL = "https://swapi.dev/api"
    settings.SWAPI_TIMEOUT = 10
    settings.CACHE_ENABLED = True
    settings.CACHE_TTL = 3600
    settings.JWT_SECRET_KEY = "test-secret-key"
    settings.JWT_ALGORITHM = "HS256"
    settings.DEBUG = True
    return settings


@pytest.fixture
def mock_swapi_character():
    """Fixture para dados mockados de um personagem."""
    return {
        "name": "Luke Skywalker",
        "height": "172",
        "mass": "77",
        "hair_color": "blond",
        "skin_color": "fair",
        "eye_color": "blue",
        "birth_year": "19BBY",
        "gender": "male",
        "homeworld": "https://swapi.dev/api/planets/1/",
        "films": [
            "https://swapi.dev/api/films/1/",
            "https://swapi.dev/api/films/2/",
        ],
        "species": ["https://swapi.dev/api/species/1/"],
        "vehicles": ["https://swapi.dev/api/vehicles/14/"],
        "starships": ["https://swapi.dev/api/starships/12/"],
        "created": "2014-12-09T13:50:51.644000Z",
        "edited": "2014-12-20T21:17:56.891000Z",
        "url": "https://swapi.dev/api/people/1/",
    }


@pytest.fixture
def mock_swapi_planet():
    """Fixture para dados mockados de um planeta."""
    return {
        "name": "Tatooine",
        "rotation_period": "23",
        "orbital_period": "304",
        "diameter": "10465",
        "climate": "arid",
        "gravity": "1 standard",
        "terrain": "desert",
        "surface_water": "1",
        "population": "200000",
        "residents": ["https://swapi.dev/api/people/1/"],
        "films": ["https://swapi.dev/api/films/1/"],
        "created": "2014-12-09T13:50:49.641000Z",
        "edited": "2014-12-20T20:58:18.411000Z",
        "url": "https://swapi.dev/api/planets/1/",
    }


@pytest.fixture
def mock_swapi_starship():
    """Fixture para dados mockados de uma nave."""
    return {
        "name": "X-wing",
        "model": "T-65 X-wing starfighter",
        "manufacturer": "Incom Corporation",
        "cost_in_credits": "149999",
        "length": "12.9",
        "max_atmosphering_speed": "1050",
        "crew": "1",
        "passengers": "0",
        "cargo_capacity": "110",
        "consumables": "5 days",
        "hyperdrive_rating": "1.0",
        "MGLT": "100",
        "starship_class": "Starfighter",
        "pilots": ["https://swapi.dev/api/people/1/"],
        "films": ["https://swapi.dev/api/films/1/"],
        "created": "2014-12-12T11:19:05.340000Z",
        "edited": "2014-12-20T21:23:49.886000Z",
        "url": "https://swapi.dev/api/starships/12/",
    }


@pytest.fixture
def mock_swapi_film():
    """Fixture para dados mockados de um filme."""
    return {
        "title": "A New Hope",
        "episode_id": 4,
        "opening_crawl": "It is a period of civil war...",
        "director": "George Lucas",
        "producer": "Gary Kurtz, Rick McCallum",
        "release_date": "1977-05-25",
        "characters": ["https://swapi.dev/api/people/1/"],
        "planets": ["https://swapi.dev/api/planets/1/"],
        "starships": ["https://swapi.dev/api/starships/12/"],
        "vehicles": ["https://swapi.dev/api/vehicles/14/"],
        "species": ["https://swapi.dev/api/species/1/"],
        "created": "2014-12-10T14:23:31.880000Z",
        "edited": "2014-12-20T19:49:45.256000Z",
        "url": "https://swapi.dev/api/films/1/",
    }


@pytest.fixture
def async_mock():
    """Fixture para criar mocks assíncronos."""
    return AsyncMock
