import logging
from typing import List, Optional, Dict, Any
from src.domain.entities.character import Character
from src.infrastructure.database.repositories.character_repository import (
    CharacterRepository,
)
from src.config.exceptions import ResourceNotFoundError

logger = logging.getLogger(__name__)


class CharacterService:
    """Serviço para gerenciar operações com personagens."""

    def __init__(self, repository: CharacterRepository):
        self.repository = repository

    async def get_character_by_id(self, character_id: str) -> Character:
        """Obtém um personagem pelo ID."""
        character = await self.repository.get_by_id(character_id)
        if not character:
            raise ResourceNotFoundError("Personagem", character_id)
        return character

    async def list_characters(
        self,
        page: int = 1,
        page_size: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        sort_by: Optional[str] = None,
        sort_order: str = "asc",
    ) -> tuple[List[Character], int]:
        """Lista personagens com filtros e ordenação."""
        return await self.repository.get_all(
            page=page,
            page_size=page_size,
            filters=filters,
            sort_by=sort_by,
            sort_order=sort_order,
        )

    async def search_characters(self, query: str) -> List[Character]:
        """Busca personagens por nome."""
        if not query or len(query) < 2:
            return []
        return await self.repository.search(query)

    async def count_characters(self) -> int:
        """Conta o total de personagens."""
        return await self.repository.count()

    async def get_characters_by_film(self, film_id: str) -> List[Character]:
        """Obtém personagens que aparecem em um filme específico."""
        from src.infrastructure.database.repositories.film_repository import (
            FilmRepository,
        )

        logger.info(f"Buscando personagens do filme {film_id}")
        characters = []

        try:
            film = await self.repository.http_client.get(
                f"https://swapi.dev/api/films/{film_id}/"
            )
            character_urls = film.get("characters", [])

            for url in character_urls:
                character_id = url.rstrip("/").split("/")[-1]
                character = await self.get_character_by_id(character_id)
                characters.append(character)

            return characters
        except Exception as e:
            logger.error(f"Erro ao buscar personagens do filme {film_id}: {str(e)}")
            return []

    async def get_characters_from_planet(self, planet_id: str) -> List[Character]:
        """Obtém personagens que são nativos de um planeta específico."""
        logger.info(f"Buscando personagens do planeta {planet_id}")
        characters = []

        try:
            planet_url = f"https://swapi.dev/api/planets/{planet_id}/"
            planet = await self.repository.http_client.get(planet_url)
            resident_urls = planet.get("residents", [])

            for url in resident_urls:
                character_id = url.rstrip("/").split("/")[-1]
                character = await self.get_character_by_id(character_id)
                characters.append(character)

            return characters
        except Exception as e:
            logger.error(f"Erro ao buscar personagens do planeta {planet_id}: {str(e)}")
            return []
