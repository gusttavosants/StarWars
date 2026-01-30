import logging
from typing import Optional, List
from fastapi import APIRouter, Depends, Query, HTTPException, status
from src.domain.entities.film import Film
from src.application.services.film_service import FilmService
from src.infrastructure.database.repositories.film_repository import FilmRepository
from src.infrastructure.http.swapi_client import SwapiClient
from src.infrastructure.cache.cache_factory import CacheFactory
from src.application.dto.filters import PaginatedResponse
from src.application.security.auth import get_optional_user
from src.config.exceptions import StarWarsAPIException

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/films", tags=["Films"])

http_client = SwapiClient()
cache = CacheFactory.create_cache()
repository = FilmRepository(http_client, cache)
service = FilmService(repository)


@router.get(
    "",
    response_model=PaginatedResponse,
    summary="Listar filmes",
    description="Lista todos os filmes com suporte a filtros, ordenação e paginação",
)
async def list_films(
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamanho da página"),
    sort_by: Optional[str] = Query(None, description="Campo para ordenar"),
    sort_order: str = Query("asc", regex="^(asc|desc)$", description="Ordem de ordenação"),
    search: Optional[str] = Query(None, description="Termo de busca"),
    current_user: Optional[str] = Depends(get_optional_user),
):
    """
    Lista todos os filmes de Star Wars.

    **Parâmetros de Query:**
    - `page`: Número da página (padrão: 1)
    - `page_size`: Itens por página (padrão: 10, máximo: 100)
    - `sort_by`: Campo para ordenar (ex: title, episode_id, release_date)
    - `sort_order`: Ordem de ordenação (asc ou desc)
    - `search`: Termo de busca por título

    **Exemplo:**
    ```
    GET /api/films?page=1&page_size=10&sort_by=episode_id&sort_order=asc
    ```
    """
    try:
        if search:
            films = await service.search_films(search)
            total = len(films)
        else:
            films, total = await service.list_films(
                page=page,
                page_size=page_size,
                sort_by=sort_by,
                sort_order=sort_order,
            )

        total_pages = (total + page_size - 1) // page_size

        return PaginatedResponse(
            items=films,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )
    except StarWarsAPIException as e:
        logger.error(f"Erro ao listar filmes: {str(e)}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Erro inesperado ao listar filmes: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao listar filmes",
        )


@router.get(
    "/{film_id}",
    response_model=Film,
    summary="Obter filme por ID",
    description="Obtém detalhes de um filme específico",
)
async def get_film(
    film_id: str,
    current_user: Optional[str] = Depends(get_optional_user),
):
    """
    Obtém detalhes de um filme específico.

    **Parâmetros:**
    - `film_id`: ID do filme (ex: 1 para A New Hope)

    **Exemplo:**
    ```
    GET /api/films/1
    ```
    """
    try:
        film = await service.get_film_by_id(film_id)
        return film
    except StarWarsAPIException as e:
        logger.error(f"Erro ao obter filme {film_id}: {str(e)}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Erro inesperado ao obter filme {film_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter filme",
        )


@router.get(
    "/search/{query}",
    response_model=List[Film],
    summary="Buscar filmes",
    description="Busca filmes por título",
)
async def search_films(
    query: str,
    current_user: Optional[str] = Depends(get_optional_user),
):
    """
    Busca filmes por título.

    **Parâmetros:**
    - `query`: Termo de busca (mínimo 2 caracteres)

    **Exemplo:**
    ```
    GET /api/films/search/hope
    ```
    """
    try:
        if len(query) < 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Termo de busca deve ter no mínimo 2 caracteres",
            )
        films = await service.search_films(query)
        return films
    except StarWarsAPIException as e:
        logger.error(f"Erro ao buscar filmes com '{query}': {str(e)}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Erro inesperado ao buscar filmes: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar filmes",
        )


@router.get(
    "/director/{director}",
    response_model=List[Film],
    summary="Filmes por diretor",
    description="Obtém filmes de um diretor específico",
)
async def get_films_by_director(
    director: str,
    current_user: Optional[str] = Depends(get_optional_user),
):
    """
    Obtém filmes de um diretor específico.

    **Parâmetros:**
    - `director`: Nome do diretor (ex: George Lucas)

    **Exemplo:**
    ```
    GET /api/films/director/George%20Lucas
    ```
    """
    try:
        films = await service.get_films_by_director(director)
        return films
    except StarWarsAPIException as e:
        logger.error(f"Erro ao obter filmes do diretor '{director}': {str(e)}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Erro inesperado ao obter filmes por diretor: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter filmes por diretor",
        )


@router.get(
    "/character/{character_id}/films",
    response_model=List[Film],
    summary="Filmes de um personagem",
    description="Obtém todos os filmes nos quais um personagem aparece",
)
async def get_films_by_character(
    character_id: str,
    current_user: Optional[str] = Depends(get_optional_user),
):
    """
    Obtém todos os filmes nos quais um personagem aparece.

    **Parâmetros:**
    - `character_id`: ID do personagem (ex: 1 para Luke Skywalker)

    **Exemplo:**
    ```
    GET /api/films/character/1/films
    ```
    """
    try:
        films = await service.get_films_by_character(character_id)
        return films
    except StarWarsAPIException as e:
        logger.error(f"Erro ao obter filmes do personagem {character_id}: {str(e)}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Erro inesperado ao obter filmes do personagem: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter filmes do personagem",
        )


@router.get(
    "/planet/{planet_id}/films",
    response_model=List[Film],
    summary="Filmes de um planeta",
    description="Obtém todos os filmes nos quais um planeta aparece",
)
async def get_films_by_planet(
    planet_id: str,
    current_user: Optional[str] = Depends(get_optional_user),
):
    """
    Obtém todos os filmes nos quais um planeta aparece.

    **Parâmetros:**
    - `planet_id`: ID do planeta (ex: 1 para Tatooine)

    **Exemplo:**
    ```
    GET /api/films/planet/1/films
    ```
    """
    try:
        films = await service.get_films_by_planet(planet_id)
        return films
    except StarWarsAPIException as e:
        logger.error(f"Erro ao obter filmes do planeta {planet_id}: {str(e)}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Erro inesperado ao obter filmes do planeta: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter filmes do planeta",
        )


@router.get(
    "/starship/{starship_id}/films",
    response_model=List[Film],
    summary="Filmes de uma nave",
    description="Obtém todos os filmes nos quais uma nave aparece",
)
async def get_films_by_starship(
    starship_id: str,
    current_user: Optional[str] = Depends(get_optional_user),
):
    """
    Obtém todos os filmes nos quais uma nave aparece.

    **Parâmetros:**
    - `starship_id`: ID da nave (ex: 12 para X-wing)

    **Exemplo:**
    ```
    GET /api/films/starship/12/films
    ```
    """
    try:
        films = await service.get_films_by_starship(starship_id)
        return films
    except StarWarsAPIException as e:
        logger.error(f"Erro ao obter filmes da nave {starship_id}: {str(e)}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Erro inesperado ao obter filmes da nave: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter filmes da nave",
        )
