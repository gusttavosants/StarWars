import logging
from typing import Optional, List
from fastapi import APIRouter, Depends, Query, HTTPException, status
from src.domain.entities.starship import Starship
from src.application.services.starship_service import StarshipService
from src.infrastructure.database.repositories.starship_repository import (
    StarshipRepository,
)
from src.infrastructure.http.swapi_client import SwapiClient
from src.infrastructure.cache.cache_factory import CacheFactory
from src.application.dto.filters import PaginatedResponse
from src.application.security.auth import get_optional_user
from src.config.exceptions import StarWarsAPIException

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/starships", tags=["Starships"])

http_client = SwapiClient()
cache = CacheFactory.create_cache()
repository = StarshipRepository(http_client, cache)
service = StarshipService(repository)


@router.get(
    "",
    response_model=PaginatedResponse,
    summary="Listar naves",
    description="Lista todas as naves estelares com suporte a filtros, ordenação e paginação",
)
async def list_starships(
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamanho da página"),
    sort_by: Optional[str] = Query(None, description="Campo para ordenar"),
    sort_order: str = Query("asc", regex="^(asc|desc)$", description="Ordem de ordenação"),
    search: Optional[str] = Query(None, description="Termo de busca"),
    current_user: Optional[str] = Depends(get_optional_user),
):
    """
    Lista todas as naves estelares de Star Wars.

    **Parâmetros de Query:**
    - `page`: Número da página (padrão: 1)
    - `page_size`: Itens por página (padrão: 10, máximo: 100)
    - `sort_by`: Campo para ordenar (ex: name, length, cost_in_credits)
    - `sort_order`: Ordem de ordenação (asc ou desc)
    - `search`: Termo de busca por nome

    **Exemplo:**
    ```
    GET /api/starships?page=1&page_size=10&sort_by=name&sort_order=asc
    ```
    """
    try:
        if search:
            starships = await service.search_starships(search)
            total = len(starships)
        else:
            starships, total = await service.list_starships(
                page=page,
                page_size=page_size,
                sort_by=sort_by,
                sort_order=sort_order,
            )

        total_pages = (total + page_size - 1) // page_size

        return PaginatedResponse(
            items=starships,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )
    except StarWarsAPIException as e:
        logger.error(f"Erro ao listar naves: {str(e)}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Erro inesperado ao listar naves: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao listar naves",
        )


@router.get(
    "/{starship_id}",
    response_model=Starship,
    summary="Obter nave por ID",
    description="Obtém detalhes de uma nave específica",
)
async def get_starship(
    starship_id: str,
    current_user: Optional[str] = Depends(get_optional_user),
):
    """
    Obtém detalhes de uma nave específica.

    **Parâmetros:**
    - `starship_id`: ID da nave (ex: 12 para X-wing)

    **Exemplo:**
    ```
    GET /api/starships/12
    ```
    """
    try:
        starship = await service.get_starship_by_id(starship_id)
        return starship
    except StarWarsAPIException as e:
        logger.error(f"Erro ao obter nave {starship_id}: {str(e)}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Erro inesperado ao obter nave {starship_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter nave",
        )


@router.get(
    "/search/{query}",
    response_model=List[Starship],
    summary="Buscar naves",
    description="Busca naves por nome",
)
async def search_starships(
    query: str,
    current_user: Optional[str] = Depends(get_optional_user),
):
    """
    Busca naves por nome.

    **Parâmetros:**
    - `query`: Termo de busca (mínimo 2 caracteres)

    **Exemplo:**
    ```
    GET /api/starships/search/x-wing
    ```
    """
    try:
        if len(query) < 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Termo de busca deve ter no mínimo 2 caracteres",
            )
        starships = await service.search_starships(query)
        return starships
    except StarWarsAPIException as e:
        logger.error(f"Erro ao buscar naves com '{query}': {str(e)}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Erro inesperado ao buscar naves: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar naves",
        )


@router.get(
    "/film/{film_id}/starships",
    response_model=List[Starship],
    summary="Naves de um filme",
    description="Obtém todas as naves que aparecem em um filme específico",
)
async def get_starships_by_film(
    film_id: str,
    current_user: Optional[str] = Depends(get_optional_user),
):
    """
    Obtém todas as naves que aparecem em um filme específico.

    **Parâmetros:**
    - `film_id`: ID do filme (ex: 1 para A New Hope)

    **Exemplo:**
    ```
    GET /api/starships/film/1/starships
    ```
    """
    try:
        starships = await service.get_starships_by_film(film_id)
        return starships
    except StarWarsAPIException as e:
        logger.error(f"Erro ao obter naves do filme {film_id}: {str(e)}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Erro inesperado ao obter naves do filme: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter naves do filme",
        )


@router.get(
    "/class/{starship_class}",
    response_model=List[Starship],
    summary="Naves por classe",
    description="Obtém naves de uma classe específica",
)
async def get_starships_by_class(
    starship_class: str,
    current_user: Optional[str] = Depends(get_optional_user),
):
    """
    Obtém naves de uma classe específica.

    **Parâmetros:**
    - `starship_class`: Classe da nave (ex: Starfighter, Transport, Capital ship)

    **Exemplo:**
    ```
    GET /api/starships/class/Starfighter
    ```
    """
    try:
        starships = await service.get_starships_by_class(starship_class)
        return starships
    except StarWarsAPIException as e:
        logger.error(f"Erro ao obter naves da classe '{starship_class}': {str(e)}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Erro inesperado ao obter naves por classe: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter naves por classe",
        )


@router.get(
    "/pilot/{pilot_id}/starships",
    response_model=List[Starship],
    summary="Naves de um piloto",
    description="Obtém todas as naves pilotadas por um personagem específico",
)
async def get_starships_by_pilot(
    pilot_id: str,
    current_user: Optional[str] = Depends(get_optional_user),
):
    """
    Obtém todas as naves pilotadas por um personagem específico.

    **Parâmetros:**
    - `pilot_id`: ID do piloto (ex: 1 para Luke Skywalker)

    **Exemplo:**
    ```
    GET /api/starships/pilot/1/starships
    ```
    """
    try:
        starships = await service.get_starships_by_pilot(pilot_id)
        return starships
    except StarWarsAPIException as e:
        logger.error(f"Erro ao obter naves do piloto {pilot_id}: {str(e)}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Erro inesperado ao obter naves do piloto: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter naves do piloto",
        )
