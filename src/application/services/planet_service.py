import logging
from typing import List, Optional, Dict, Any
from src.domain.entities.planet import Planet
from src.infrastructure.database.repositories.planet_repository import (
    PlanetRepository,
)
from src.config.exceptions import ResourceNotFoundError

logger = logging.getLogger(__name__)


class PlanetService:
    """Serviço para gerenciar operações com planetas."""

    def __init__(self, repository: PlanetRepository):
        self.repository = repository

    async def get_planet_by_id(self, planet_id: str) -> Planet:
        """Obtém um planeta pelo ID."""
        planet = await self.repository.get_by_id(planet_id)
        if not planet:
            raise ResourceNotFoundError("Planeta", planet_id)
        return planet

    async def list_planets(
        self,
        page: int = 1,
        page_size: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        sort_by: Optional[str] = None,
        sort_order: str = "asc",
    ) -> tuple[List[Planet], int]:
        """Lista planetas com filtros e ordenação."""
        return await self.repository.get_all(
            page=page,
            page_size=page_size,
            filters=filters,
            sort_by=sort_by,
            sort_order=sort_order,
        )

    async def search_planets(self, query: str) -> List[Planet]:
        """Busca planetas por nome."""
        if not query or len(query) < 2:
            return []
        return await self.repository.search(query)

    async def count_planets(self) -> int:
        """Conta o total de planetas."""
        return await self.repository.count()

    async def get_planets_by_film(self, film_id: str) -> List[Planet]:
        """Obtém planetas que aparecem em um filme específico."""
        logger.info(f"Buscando planetas do filme {film_id}")
        planets = []

        try:
            film = await self.repository.http_client.get(
                f"https://swapi.dev/api/films/{film_id}/"
            )
            planet_urls = film.get("planets", [])

            for url in planet_urls:
                planet_id = url.rstrip("/").split("/")[-1]
                planet = await self.get_planet_by_id(planet_id)
                planets.append(planet)

            return planets
        except Exception as e:
            logger.error(f"Erro ao buscar planetas do filme {film_id}: {str(e)}")
            return []

    async def get_planets_by_climate(self, climate: str) -> List[Planet]:
        """Obtém planetas com um clima específico."""
        logger.info(f"Buscando planetas com clima '{climate}'")
        planets, _ = await self.list_planets(
            filters={"climate": {"operator": "contains", "value": climate}}
        )
        return planets
