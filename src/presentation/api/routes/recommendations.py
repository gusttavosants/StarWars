import logging
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from src.application.services.recommendation_service import RecommendationService
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

router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])

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

recommendation_service = RecommendationService()


@router.get(
    "/character/{character_id}",
    summary="Recomendações para Personagem",
    description="Obtém recomendações relacionadas a um personagem",
)
async def get_character_recommendations(
    character_id: str,
    current_user: Optional[str] = Depends(get_optional_user),
):
    """Retorna recomendações relacionadas a um personagem."""
    try:
        await recommendation_service.track_view(current_user or "anonymous", character_id, "character")
        
        recommendations = await recommendation_service.get_recommendations_for_character(
            character_id,
            character_service,
            film_service,
            starship_service,
        )
        
        return recommendations
    except Exception as e:
        logger.error(f"Erro ao obter recomendações: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter recomendações",
        )


@router.get(
    "/film/{film_id}",
    summary="Recomendações para Filme",
    description="Obtém recomendações relacionadas a um filme",
)
async def get_film_recommendations(
    film_id: str,
    current_user: Optional[str] = Depends(get_optional_user),
):
    """Retorna recomendações relacionadas a um filme."""
    try:
        await recommendation_service.track_view(current_user or "anonymous", film_id, "film")
        
        recommendations = await recommendation_service.get_recommendations_for_film(
            film_id,
            film_service,
            character_service,
            planet_service,
        )
        
        return recommendations
    except Exception as e:
        logger.error(f"Erro ao obter recomendações: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter recomendações",
        )


@router.get(
    "/trending",
    summary="Recursos em Alta",
    description="Obtém recursos mais visualizados (em alta)",
)
async def get_trending_resources(
    current_user: Optional[str] = Depends(get_optional_user),
):
    """Retorna recursos em alta."""
    try:
        trending = await recommendation_service.get_trending_resources()
        return trending
    except Exception as e:
        logger.error(f"Erro ao obter trending: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter trending",
        )
