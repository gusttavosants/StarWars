import logging
from typing import List, Optional, Dict, Any
from src.domain.entities.film import Film
from src.infrastructure.database.repositories.film_repository import FilmRepository
from src.config.exceptions import ResourceNotFoundError

logger = logging.getLogger(__name__)


class FilmService:
    """Serviço para gerenciar operações com filmes."""

    def __init__(self, repository: FilmRepository):
        self.repository = repository

    async def get_film_by_id(self, film_id: str) -> Film:
        """Obtém um filme pelo ID."""
        film = await self.repository.get_by_id(film_id)
        if not film:
            raise ResourceNotFoundError("Filme", film_id)
        return film

    async def list_films(
        self,
        page: int = 1,
        page_size: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        sort_by: Optional[str] = None,
        sort_order: str = "asc",
    ) -> tuple[List[Film], int]:
        """Lista filmes com filtros e ordenação."""
        return await self.repository.get_all(
            page=page,
            page_size=page_size,
            filters=filters,
            sort_by=sort_by,
            sort_order=sort_order,
        )

    async def search_films(self, query: str) -> List[Film]:
        """Busca filmes por título."""
        if not query or len(query) < 2:
            return []
        return await self.repository.search(query)

    async def count_films(self) -> int:
        """Conta o total de filmes."""
        return await self.repository.count()

    async def get_films_by_director(self, director: str) -> List[Film]:
        """Obtém filmes de um diretor específico."""
        logger.info(f"Buscando filmes do diretor '{director}'")
        films, _ = await self.list_films(
            filters={"director": {"operator": "contains", "value": director}}
        )
        return films

    async def get_films_by_character(self, character_id: str) -> List[Film]:
        """Obtém filmes nos quais um personagem aparece."""
        logger.info(f"Buscando filmes do personagem {character_id}")
        films = []

        try:
            character = await self.repository.http_client.get(
                f"https://swapi.dev/api/people/{character_id}/"
            )
            film_urls = character.get("films", [])

            for url in film_urls:
                film_id = url.rstrip("/").split("/")[-1]
                film = await self.get_film_by_id(film_id)
                films.append(film)

            return films
        except Exception as e:
            logger.error(f"Erro ao buscar filmes do personagem {character_id}: {str(e)}")
            return []

    async def get_films_by_planet(self, planet_id: str) -> List[Film]:
        """Obtém filmes nos quais um planeta aparece."""
        logger.info(f"Buscando filmes do planeta {planet_id}")
        films = []

        try:
            planet = await self.repository.http_client.get(
                f"https://swapi.dev/api/planets/{planet_id}/"
            )
            film_urls = planet.get("films", [])

            for url in film_urls:
                film_id = url.rstrip("/").split("/")[-1]
                film = await self.get_film_by_id(film_id)
                films.append(film)

            return films
        except Exception as e:
            logger.error(f"Erro ao buscar filmes do planeta {planet_id}: {str(e)}")
            return []

    async def get_films_by_starship(self, starship_id: str) -> List[Film]:
        """Obtém filmes nos quais uma nave aparece."""
        logger.info(f"Buscando filmes da nave {starship_id}")
        films = []

        try:
            starship = await self.repository.http_client.get(
                f"https://swapi.dev/api/starships/{starship_id}/"
            )
            film_urls = starship.get("films", [])

            for url in film_urls:
                film_id = url.rstrip("/").split("/")[-1]
                film = await self.get_film_by_id(film_id)
                films.append(film)

            return films
        except Exception as e:
            logger.error(f"Erro ao buscar filmes da nave {starship_id}: {str(e)}")
            return []
