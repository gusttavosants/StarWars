import pytest

from src.domain.entities.character import Character
from src.domain.entities.film import Film
from src.domain.entities.planet import Planet
from src.domain.entities.starship import Starship


class TestCharacterEntity:
    """Testes para entidade Character."""

    def test_character_creation_success(self, mock_swapi_character):
        """Testa criação de personagem com sucesso."""
        character = Character(**mock_swapi_character)

        assert character.name == "Luke Skywalker"
        assert character.height == "172"
        assert character.mass == "77"
        assert character.gender == "male"

    def test_character_with_minimal_data(self):
        """Testa criação de personagem com dados mínimos."""
        character = Character(name="Luke Skywalker")

        assert character.name == "Luke Skywalker"
        assert character.height is None
        assert character.mass is None

    def test_character_get_id(self, mock_swapi_character):
        """Testa extração de ID da URL."""
        character = Character(**mock_swapi_character)
        character_id = character.get_id()

        assert character_id == "1"

    def test_character_get_id_without_url(self):
        """Testa extração de ID quando não há URL."""
        character = Character(name="Luke Skywalker")
        character_id = character.get_id()

        assert character_id is None

    def test_character_films_list(self, mock_swapi_character):
        """Testa lista de filmes."""
        character = Character(**mock_swapi_character)

        assert isinstance(character.films, list)
        assert len(character.films) > 0

    def test_character_species_list(self, mock_swapi_character):
        """Testa lista de espécies."""
        character = Character(**mock_swapi_character)

        assert isinstance(character.species, list)

    def test_character_vehicles_list(self, mock_swapi_character):
        """Testa lista de veículos."""
        character = Character(**mock_swapi_character)

        assert isinstance(character.vehicles, list)

    def test_character_starships_list(self, mock_swapi_character):
        """Testa lista de naves."""
        character = Character(**mock_swapi_character)

        assert isinstance(character.starships, list)

    def test_character_json_schema(self):
        """Testa schema JSON do personagem."""
        character = Character(name="Luke Skywalker")
        schema = character.model_json_schema()

        assert "properties" in schema
        assert "name" in schema["properties"]


class TestPlanetEntity:
    """Testes para entidade Planet."""

    def test_planet_creation_success(self, mock_swapi_planet):
        """Testa criação de planeta com sucesso."""
        planet = Planet(**mock_swapi_planet)

        assert planet.name == "Tatooine"
        assert planet.climate == "arid"
        assert planet.terrain == "desert"

    def test_planet_with_minimal_data(self):
        """Testa criação de planeta com dados mínimos."""
        planet = Planet(name="Tatooine")

        assert planet.name == "Tatooine"
        assert planet.climate is None
        assert planet.population is None

    def test_planet_get_id(self, mock_swapi_planet):
        """Testa extração de ID da URL."""
        planet = Planet(**mock_swapi_planet)
        planet_id = planet.get_id()

        assert planet_id == "1"

    def test_planet_residents_list(self, mock_swapi_planet):
        """Testa lista de residentes."""
        planet = Planet(**mock_swapi_planet)

        assert isinstance(planet.residents, list)

    def test_planet_films_list(self, mock_swapi_planet):
        """Testa lista de filmes."""
        planet = Planet(**mock_swapi_planet)

        assert isinstance(planet.films, list)

    def test_planet_numeric_fields(self, mock_swapi_planet):
        """Testa campos numéricos."""
        planet = Planet(**mock_swapi_planet)

        assert planet.diameter == "10465"
        assert planet.surface_water == "1"
        assert planet.population == "200000"


class TestStarshipEntity:
    """Testes para entidade Starship."""

    def test_starship_creation_success(self, mock_swapi_starship):
        """Testa criação de nave com sucesso."""
        starship = Starship(**mock_swapi_starship)

        assert starship.name == "X-wing"
        assert starship.model == "T-65 X-wing starfighter"
        assert starship.starship_class == "Starfighter"

    def test_starship_with_minimal_data(self):
        """Testa criação de nave com dados mínimos."""
        starship = Starship(name="X-wing")

        assert starship.name == "X-wing"
        assert starship.model is None
        assert starship.manufacturer is None

    def test_starship_get_id(self, mock_swapi_starship):
        """Testa extração de ID da URL."""
        starship = Starship(**mock_swapi_starship)
        starship_id = starship.get_id()

        assert starship_id == "12"

    def test_starship_pilots_list(self, mock_swapi_starship):
        """Testa lista de pilotos."""
        starship = Starship(**mock_swapi_starship)

        assert isinstance(starship.pilots, list)

    def test_starship_films_list(self, mock_swapi_starship):
        """Testa lista de filmes."""
        starship = Starship(**mock_swapi_starship)

        assert isinstance(starship.films, list)

    def test_starship_mglt_field(self, mock_swapi_starship):
        """Testa campo MGLT (alias)."""
        starship = Starship(**mock_swapi_starship)

        assert starship.mglt == "100"

    def test_starship_numeric_fields(self, mock_swapi_starship):
        """Testa campos numéricos."""
        starship = Starship(**mock_swapi_starship)

        assert starship.length == "12.9"
        assert starship.max_atmosphering_speed == "1050"
        assert starship.crew == "1"
        assert starship.passengers == "0"


class TestFilmEntity:
    """Testes para entidade Film."""

    def test_film_creation_success(self, mock_swapi_film):
        """Testa criação de filme com sucesso."""
        film = Film(**mock_swapi_film)

        assert film.title == "A New Hope"
        assert film.episode_id == 4
        assert film.director == "George Lucas"

    def test_film_with_minimal_data(self):
        """Testa criação de filme com dados mínimos."""
        film = Film(title="A New Hope")

        assert film.title == "A New Hope"
        assert film.episode_id is None
        assert film.director is None

    def test_film_get_id(self, mock_swapi_film):
        """Testa extração de ID da URL."""
        film = Film(**mock_swapi_film)
        film_id = film.get_id()

        assert film_id == "1"

    def test_film_characters_list(self, mock_swapi_film):
        """Testa lista de personagens."""
        film = Film(**mock_swapi_film)

        assert isinstance(film.characters, list)

    def test_film_planets_list(self, mock_swapi_film):
        """Testa lista de planetas."""
        film = Film(**mock_swapi_film)

        assert isinstance(film.planets, list)

    def test_film_starships_list(self, mock_swapi_film):
        """Testa lista de naves."""
        film = Film(**mock_swapi_film)

        assert isinstance(film.starships, list)

    def test_film_vehicles_list(self, mock_swapi_film):
        """Testa lista de veículos."""
        film = Film(**mock_swapi_film)

        assert isinstance(film.vehicles, list)

    def test_film_species_list(self, mock_swapi_film):
        """Testa lista de espécies."""
        film = Film(**mock_swapi_film)

        assert isinstance(film.species, list)

    def test_film_release_date(self, mock_swapi_film):
        """Testa data de lançamento."""
        film = Film(**mock_swapi_film)

        assert film.release_date == "1977-05-25"

    def test_film_opening_crawl(self, mock_swapi_film):
        """Testa texto de abertura."""
        film = Film(**mock_swapi_film)

        assert film.opening_crawl == "It is a period of civil war..."


class TestEntitySerialization:
    """Testes para serialização de entidades."""

    def test_character_to_dict(self, mock_swapi_character):
        """Testa conversão de Character para dict."""
        character = Character(**mock_swapi_character)
        data = character.model_dump()

        assert isinstance(data, dict)
        assert data["name"] == "Luke Skywalker"

    def test_character_to_json(self, mock_swapi_character):
        """Testa conversão de Character para JSON."""
        character = Character(**mock_swapi_character)
        json_str = character.model_dump_json()

        assert isinstance(json_str, str)
        assert "Luke Skywalker" in json_str

    def test_planet_to_dict(self, mock_swapi_planet):
        """Testa conversão de Planet para dict."""
        planet = Planet(**mock_swapi_planet)
        data = planet.model_dump()

        assert isinstance(data, dict)
        assert data["name"] == "Tatooine"

    def test_starship_to_dict(self, mock_swapi_starship):
        """Testa conversão de Starship para dict."""
        starship = Starship(**mock_swapi_starship)
        data = starship.model_dump()

        assert isinstance(data, dict)
        assert data["name"] == "X-wing"

    def test_film_to_dict(self, mock_swapi_film):
        """Testa conversão de Film para dict."""
        film = Film(**mock_swapi_film)
        data = film.model_dump()

        assert isinstance(data, dict)
        assert data["title"] == "A New Hope"
