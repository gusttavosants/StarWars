import logging
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional, List
from src.application.services.advanced_search_service import AdvancedSearchService
from src.application.services.character_service import CharacterService
from src.application.services.film_service import FilmService
from src.application.services.planet_service import PlanetService
from src.application.services.starship_service import StarshipService
from src.infrastructure.database.repositories.character_repository import CharacterRepository
from src.infrastructure.database.repositories.film_repository import FilmRepository
from src.infrastructure.database.repositories.planet_repository import PlanetRepository
from src.infrastructure.database.repositories.starship_repository import StarshipRepository
from src.infrastructure.http.swapi_client import SwapiClient
from src.infrastructure.cache.cache_factory import CacheFactory
from src.application.security.auth import get_optional_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/search", tags=["Advanced Search"])

http_client = SwapiClient()
cache = CacheFactory.create_cache()

character_repo = CharacterRepository(http_client, cache)
film_repo = FilmRepository(http_client, cache)
planet_repo = PlanetRepository(http_client, cache)
starship_repo = StarshipRepository(http_client, cache)

character_service = CharacterService(character_repo)
film_service = FilmService(film_repo)
planet_service = PlanetService(planet_repo)
starship_service = StarshipService(starship_repo)

search_service = AdvancedSearchService()


@router.get(
    "/advanced",
    summary="Busca Avançada com Scoring",
    description="Busca avançada com scoring de relevância",
)
async def advanced_search(
    query: str = Query(..., min_length=2, description="Termo de busca"),
    resource_type: str = Query("all", description="Tipo de recurso: all, characters, films, planets, starships"),
    min_score: float = Query(0.3, ge=0, le=1, description="Score mínimo de relevância"),
    limit: int = Query(10, ge=1, le=100, description="Número máximo de resultados"),
    current_user: Optional[str] = Depends(get_optional_user),
):
    """Realiza busca avançada com scoring de relevância."""
    try:
        results = {}

        if resource_type in ["all", "characters"]:
            characters, _ = await character_service.list_characters(page_size=1000)
            char_results = await search_service.search_with_scoring(
                query,
                [{"name": c.name, "id": c.get_id()} for c in characters],
                ["name"],
                min_score,
            )
            results["characters"] = [
                {"name": r[0]["name"], "id": r[0]["id"], "relevance_score": round(r[1], 2)}
                for r in char_results[:limit]
            ]

        if resource_type in ["all", "films"]:
            films, _ = await film_service.list_films(page_size=1000)
            film_results = await search_service.search_with_scoring(
                query,
                [{"title": f.title, "id": f.get_id()} for f in films],
                ["title"],
                min_score,
            )
            results["films"] = [
                {"title": r[0]["title"], "id": r[0]["id"], "relevance_score": round(r[1], 2)}
                for r in film_results[:limit]
            ]

        if resource_type in ["all", "planets"]:
            planets, _ = await planet_service.list_planets(page_size=1000)
            planet_results = await search_service.search_with_scoring(
                query,
                [{"name": p.name, "id": p.get_id()} for p in planets],
                ["name"],
                min_score,
            )
            results["planets"] = [
                {"name": r[0]["name"], "id": r[0]["id"], "relevance_score": round(r[1], 2)}
                for r in planet_results[:limit]
            ]

        if resource_type in ["all", "starships"]:
            starships, _ = await starship_service.list_starships(page_size=1000)
            starship_results = await search_service.search_with_scoring(
                query,
                [{"name": s.name, "id": s.get_id()} for s in starships],
                ["name"],
                min_score,
            )
            results["starships"] = [
                {"name": r[0]["name"], "id": r[0]["id"], "relevance_score": round(r[1], 2)}
                for r in starship_results[:limit]
            ]

        return {"query": query, "results": results}
    except Exception as e:
        logger.error(f"Erro na busca avançada: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro na busca avançada",
        )


@router.get(
    "/autocomplete",
    summary="Autocompletar",
    description="Sugestões de autocompletar",
)
async def autocomplete(
    query: str = Query(..., min_length=1, description="Termo de busca"),
    resource_type: str = Query("all", description="Tipo de recurso"),
    limit: int = Query(5, ge=1, le=20, description="Número máximo de sugestões"),
    current_user: Optional[str] = Depends(get_optional_user),
):
    """Retorna sugestões de autocompletar."""
    try:
        suggestions = {}

        if resource_type in ["all", "characters"]:
            characters, _ = await character_service.list_characters(page_size=1000)
            char_data = [{"name": c.name} for c in characters]
            suggestions["characters"] = await search_service.autocomplete(
                query, char_data, "name", limit
            )

        if resource_type in ["all", "films"]:
            films, _ = await film_service.list_films(page_size=1000)
            film_data = [{"title": f.title} for f in films]
            suggestions["films"] = await search_service.autocomplete(
                query, film_data, "title", limit
            )

        return suggestions
    except Exception as e:
        logger.error(f"Erro no autocompletar: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro no autocompletar",
        )
