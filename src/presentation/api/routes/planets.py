import logging
from typing import Optional, List
from fastapi import APIRouter, Depends, Query, HTTPException, status
from src.domain.entities.planet import Planet
from src.application.services.planet_service import PlanetService
from src.infrastructure.database.repositories.planet_repository import (
    PlanetRepository,
)
from src.infrastructure.http.swapi_client import SwapiClient
from src.infrastructure.cache.cache_factory import CacheFactory
from src.application.dto.filters import PaginatedResponse
from src.application.security.auth import get_optional_user
from src.config.exceptions import StarWarsAPIException

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/planets", tags=["Planets"])

http_client = SwapiClient()
cache = CacheFactory.create_cache()
repository = PlanetRepository(http_client, cache)
service = PlanetService(repository)


@router.get(
    "",
    response_model=PaginatedResponse,
    summary="Listar planetas",
    description="Lista todos os planetas com suporte a filtros, ordenação e paginação",
)
async def list_planets(
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamanho da página"),
    sort_by: Optional[str] = Query(None, description="Campo para ordenar"),
    sort_order: str = Query("asc", regex="^(asc|desc)$", description="Ordem de ordenação"),
    search: Optional[str] = Query(None, description="Termo de busca"),
    current_user: Optional[str] = Depends(get_optional_user),
):
    """
    Lista todos os planetas de Star Wars.

    **Parâmetros de Query:**
    - `page`: Número da página (padrão: 1)
    - `page_size`: Itens por página (padrão: 10, máximo: 100)
    - `sort_by`: Campo para ordenar (ex: name, diameter, population)
    - `sort_order`: Ordem de ordenação (asc ou desc)
    - `search`: Termo de busca por nome

    **Exemplo:**
    ```
    GET /api/planets?page=1&page_size=10&sort_by=name&sort_order=asc
    ```
    """
    try:
        if search:
            planets = await service.search_planets(search)
            total = len(planets)
        else:
            planets, total = await service.list_planets(
                page=page,
                page_size=page_size,
                sort_by=sort_by,
                sort_order=sort_order,
            )

        total_pages = (total + page_size - 1) // page_size

        return PaginatedResponse(
            items=planets,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )
    except StarWarsAPIException as e:
        logger.error(f"Erro ao listar planetas: {str(e)}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Erro inesperado ao listar planetas: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao listar planetas",
        )


@router.get(
    "/{planet_id}",
    response_model=Planet,
    summary="Obter planeta por ID",
    description="Obtém detalhes de um planeta específico",
)
async def get_planet(
    planet_id: str,
    current_user: Optional[str] = Depends(get_optional_user),
):
    """
    Obtém detalhes de um planeta específico.

    **Parâmetros:**
    - `planet_id`: ID do planeta (ex: 1 para Tatooine)

    **Exemplo:**
    ```
    GET /api/planets/1
    ```
    """
    try:
        planet = await service.get_planet_by_id(planet_id)
        return planet
    except StarWarsAPIException as e:
        logger.error(f"Erro ao obter planeta {planet_id}: {str(e)}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Erro inesperado ao obter planeta {planet_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter planeta",
        )


@router.get(
    "/search/{query}",
    response_model=List[Planet],
    summary="Buscar planetas",
    description="Busca planetas por nome",
)
async def search_planets(
    query: str,
    current_user: Optional[str] = Depends(get_optional_user),
):
    """
    Busca planetas por nome.

    **Parâmetros:**
    - `query`: Termo de busca (mínimo 2 caracteres)

    **Exemplo:**
    ```
    GET /api/planets/search/tatooine
    ```
    """
    try:
        if len(query) < 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Termo de busca deve ter no mínimo 2 caracteres",
            )
        planets = await service.search_planets(query)
        return planets
    except StarWarsAPIException as e:
        logger.error(f"Erro ao buscar planetas com '{query}': {str(e)}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Erro inesperado ao buscar planetas: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar planetas",
        )


@router.get(
    "/film/{film_id}/planets",
    response_model=List[Planet],
    summary="Planetas de um filme",
    description="Obtém todos os planetas que aparecem em um filme específico",
)
async def get_planets_by_film(
    film_id: str,
    current_user: Optional[str] = Depends(get_optional_user),
):
    """
    Obtém todos os planetas que aparecem em um filme específico.

    **Parâmetros:**
    - `film_id`: ID do filme (ex: 1 para A New Hope)

    **Exemplo:**
    ```
    GET /api/planets/film/1/planets
    ```
    """
    try:
        planets = await service.get_planets_by_film(film_id)
        return planets
    except StarWarsAPIException as e:
        logger.error(f"Erro ao obter planetas do filme {film_id}: {str(e)}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Erro inesperado ao obter planetas do filme: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter planetas do filme",
        )


@router.get(
    "/climate/{climate}",
    response_model=List[Planet],
    summary="Planetas por clima",
    description="Obtém planetas com um clima específico",
)
async def get_planets_by_climate(
    climate: str,
    current_user: Optional[str] = Depends(get_optional_user),
):
    """
    Obtém planetas com um clima específico.

    **Parâmetros:**
    - `climate`: Tipo de clima (ex: arid, temperate, tropical)

    **Exemplo:**
    ```
    GET /api/planets/climate/arid
    ```
    """
    try:
        planets = await service.get_planets_by_climate(climate)
        return planets
    except StarWarsAPIException as e:
        logger.error(f"Erro ao obter planetas com clima '{climate}': {str(e)}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Erro inesperado ao obter planetas por clima: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter planetas por clima",
        )
