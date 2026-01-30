import logging
from typing import List, Optional, Dict, Any
from src.domain.entities.starship import Starship
from src.infrastructure.database.repositories.starship_repository import (
    StarshipRepository,
)
from src.config.exceptions import ResourceNotFoundError

logger = logging.getLogger(__name__)


class StarshipService:
    """Serviço para gerenciar operações com naves estelares."""

    def __init__(self, repository: StarshipRepository):
        self.repository = repository

    async def get_starship_by_id(self, starship_id: str) -> Starship:
        """Obtém uma nave pelo ID."""
        starship = await self.repository.get_by_id(starship_id)
        if not starship:
            raise ResourceNotFoundError("Nave", starship_id)
        return starship

    async def list_starships(
        self,
        page: int = 1,
        page_size: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        sort_by: Optional[str] = None,
        sort_order: str = "asc",
    ) -> tuple[List[Starship], int]:
        """Lista naves com filtros e ordenação."""
        return await self.repository.get_all(
            page=page,
            page_size=page_size,
            filters=filters,
            sort_by=sort_by,
            sort_order=sort_order,
        )

    async def search_starships(self, query: str) -> List[Starship]:
        """Busca naves por nome."""
        if not query or len(query) < 2:
            return []
        return await self.repository.search(query)

    async def count_starships(self) -> int:
        """Conta o total de naves."""
        return await self.repository.count()

    async def get_starships_by_film(self, film_id: str) -> List[Starship]:
        """Obtém naves que aparecem em um filme específico."""
        logger.info(f"Buscando naves do filme {film_id}")
        starships = []

        try:
            film = await self.repository.http_client.get(
                f"https://swapi.dev/api/films/{film_id}/"
            )
            starship_urls = film.get("starships", [])

            for url in starship_urls:
                starship_id = url.rstrip("/").split("/")[-1]
                starship = await self.get_starship_by_id(starship_id)
                starships.append(starship)

            return starships
        except Exception as e:
            logger.error(f"Erro ao buscar naves do filme {film_id}: {str(e)}")
            return []

    async def get_starships_by_class(self, starship_class: str) -> List[Starship]:
        """Obtém naves de uma classe específica."""
        logger.info(f"Buscando naves da classe '{starship_class}'")
        starships, _ = await self.list_starships(
            filters={"starship_class": {"operator": "contains", "value": starship_class}}
        )
        return starships

    async def get_starships_by_pilot(self, pilot_id: str) -> List[Starship]:
        """Obtém naves pilotadas por um personagem específico."""
        logger.info(f"Buscando naves do piloto {pilot_id}")
        starships = []

        try:
            pilot_url = f"https://swapi.dev/api/people/{pilot_id}/"
            pilot = await self.repository.http_client.get(pilot_url)
            starship_urls = pilot.get("starships", [])

            for url in starship_urls:
                starship_id = url.rstrip("/").split("/")[-1]
                starship = await self.get_starship_by_id(starship_id)
                starships.append(starship)

            return starships
        except Exception as e:
            logger.error(f"Erro ao buscar naves do piloto {pilot_id}: {str(e)}")
            return []
