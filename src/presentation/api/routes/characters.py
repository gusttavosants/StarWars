import logging
from typing import Optional, List
from fastapi import APIRouter, Depends, Query, HTTPException, status
from src.domain.entities.character import Character
from src.application.services.character_service import CharacterService
from src.infrastructure.database.repositories.character_repository import (
    CharacterRepository,
)
from src.infrastructure.http.swapi_client import SwapiClient
from src.infrastructure.cache.cache_factory import CacheFactory
from src.application.dto.filters import PaginatedResponse, ErrorResponse
from src.application.security.auth import get_optional_user
from src.config.exceptions import StarWarsAPIException

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/characters", tags=["Characters"])

http_client = SwapiClient()
cache = CacheFactory.create_cache()
repository = CharacterRepository(http_client, cache)
service = CharacterService(repository)


@router.get(
    "",
    response_model=PaginatedResponse,
    summary="Listar personagens",
    description="Lista todos os personagens com suporte a filtros, ordenação e paginação",
)
async def list_characters(
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamanho da página"),
    sort_by: Optional[str] = Query(None, description="Campo para ordenar"),
    sort_order: str = Query("asc", regex="^(asc|desc)$", description="Ordem de ordenação"),
    search: Optional[str] = Query(None, description="Termo de busca"),
    current_user: Optional[str] = Depends(get_optional_user),
):
    """
    Lista todos os personagens de Star Wars.

    **Parâmetros de Query:**
    - `page`: Número da página (padrão: 1)
    - `page_size`: Itens por página (padrão: 10, máximo: 100)
    - `sort_by`: Campo para ordenar (ex: name, height, mass)
    - `sort_order`: Ordem de ordenação (asc ou desc)
    - `search`: Termo de busca por nome

    **Exemplo:**
    ```
    GET /api/characters?page=1&page_size=10&sort_by=name&sort_order=asc
    ```
    """
    try:
        if search:
            characters = await service.search_characters(search)
            total = len(characters)
        else:
            characters, total = await service.list_characters(
                page=page,
                page_size=page_size,
                sort_by=sort_by,
                sort_order=sort_order,
            )

        total_pages = (total + page_size - 1) // page_size

        return PaginatedResponse(
            items=characters,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )
    except StarWarsAPIException as e:
        logger.error(f"Erro ao listar personagens: {str(e)}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Erro inesperado ao listar personagens: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao listar personagens",
        )


@router.get(
    "/{character_id}",
    response_model=Character,
    summary="Obter personagem por ID",
    description="Obtém detalhes de um personagem específico",
)
async def get_character(
    character_id: str,
    current_user: Optional[str] = Depends(get_optional_user),
):
    """
    Obtém detalhes de um personagem específico.

    **Parâmetros:**
    - `character_id`: ID do personagem (ex: 1 para Luke Skywalker)

    **Exemplo:**
    ```
    GET /api/characters/1
    ```
    """
    try:
        character = await service.get_character_by_id(character_id)
        return character
    except StarWarsAPIException as e:
        logger.error(f"Erro ao obter personagem {character_id}: {str(e)}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Erro inesperado ao obter personagem {character_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter personagem",
        )


@router.get(
    "/search/{query}",
    response_model=List[Character],
    summary="Buscar personagens",
    description="Busca personagens por nome",
)
async def search_characters(
    query: str,
    current_user: Optional[str] = Depends(get_optional_user),
):
    """
    Busca personagens por nome.

    **Parâmetros:**
    - `query`: Termo de busca (mínimo 2 caracteres)

    **Exemplo:**
    ```
    GET /api/characters/search/luke
    ```
    """
    try:
        if len(query) < 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Termo de busca deve ter no mínimo 2 caracteres",
            )
        characters = await service.search_characters(query)
        return characters
    except StarWarsAPIException as e:
        logger.error(f"Erro ao buscar personagens com '{query}': {str(e)}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Erro inesperado ao buscar personagens: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar personagens",
        )


@router.get(
    "/film/{film_id}/characters",
    response_model=List[Character],
    summary="Personagens de um filme",
    description="Obtém todos os personagens que aparecem em um filme específico",
)
async def get_characters_by_film(
    film_id: str,
    current_user: Optional[str] = Depends(get_optional_user),
):
    """
    Obtém todos os personagens que aparecem em um filme específico.

    **Parâmetros:**
    - `film_id`: ID do filme (ex: 1 para A New Hope)

    **Exemplo:**
    ```
    GET /api/characters/film/1/characters
    ```
    """
    try:
        characters = await service.get_characters_by_film(film_id)
        return characters
    except StarWarsAPIException as e:
        logger.error(f"Erro ao obter personagens do filme {film_id}: {str(e)}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Erro inesperado ao obter personagens do filme: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter personagens do filme",
        )


@router.get(
    "/planet/{planet_id}/residents",
    response_model=List[Character],
    summary="Residentes de um planeta",
    description="Obtém todos os personagens nativos de um planeta específico",
)
async def get_characters_from_planet(
    planet_id: str,
    current_user: Optional[str] = Depends(get_optional_user),
):
    """
    Obtém todos os personagens nativos de um planeta específico.

    **Parâmetros:**
    - `planet_id`: ID do planeta (ex: 1 para Tatooine)

    **Exemplo:**
    ```
    GET /api/characters/planet/1/residents
    ```
    """
    try:
        characters = await service.get_characters_from_planet(planet_id)
        return characters
    except StarWarsAPIException as e:
        logger.error(f"Erro ao obter residentes do planeta {planet_id}: {str(e)}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Erro inesperado ao obter residentes do planeta: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter residentes do planeta",
        )
