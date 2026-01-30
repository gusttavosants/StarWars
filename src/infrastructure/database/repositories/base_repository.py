import logging
from typing import List, Optional, TypeVar, Generic, Dict, Any
from src.domain.interfaces.repository import IRepository
from src.domain.interfaces.client import IHttpClient
from src.domain.interfaces.cache import ICache
from src.config.settings import settings
from src.config.exceptions import ResourceNotFoundError, InvalidFilterError

logger = logging.getLogger(__name__)

T = TypeVar("T")


class BaseRepository(IRepository[T], Generic[T]):
    """Classe base para repositórios."""

    def __init__(
        self,
        http_client: IHttpClient,
        cache: ICache,
        resource_type: str,
        entity_class: type[T],
    ):
        self.http_client = http_client
        self.cache = cache
        self.resource_type = resource_type
        self.entity_class = entity_class

    def _build_url(self, path: str = "") -> str:
        """Constrói a URL para o recurso."""
        base_url = settings.SWAPI_BASE_URL
        if path:
            return f"{base_url}/{self.resource_type}/{path}/"
        return f"{base_url}/{self.resource_type}/"

    def _get_cache_key(self, *args) -> str:
        """Gera uma chave de cache."""
        return f"{self.resource_type}:{'_'.join(str(arg) for arg in args)}"

    async def get_by_id(self, resource_id: str) -> Optional[T]:
        """Obtém um recurso pelo ID."""
        cache_key = self._get_cache_key("by_id", resource_id)

        if settings.CACHE_ENABLED:
            cached = await self.cache.get(cache_key)
            if cached:
                logger.debug(f"Cache hit para {cache_key}")
                return self.entity_class(**cached)

        try:
            url = self._build_url(resource_id)
            data = await self.http_client.get(url)
            entity = self.entity_class(**data)

            if settings.CACHE_ENABLED:
                await self.cache.set(cache_key, data, settings.CACHE_TTL)

            return entity
        except Exception as e:
            logger.error(f"Erro ao obter {self.resource_type} com ID {resource_id}: {str(e)}")
            raise ResourceNotFoundError(self.resource_type, resource_id)

    async def get_all(
        self,
        page: int = 1,
        page_size: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        sort_by: Optional[str] = None,
        sort_order: str = "asc",
    ) -> tuple[List[T], int]:
        """Obtém todos os recursos com paginação, filtros e ordenação."""
        cache_key = self._get_cache_key(
            "all",
            page,
            page_size,
            str(filters),
            sort_by,
            sort_order,
        )

        if settings.CACHE_ENABLED:
            cached = await self.cache.get(cache_key)
            if cached:
                logger.debug(f"Cache hit para {cache_key}")
                entities = [self.entity_class(**item) for item in cached["items"]]
                return entities, cached["total"]

        try:
            url = self._build_url()
            params = {"page": page}

            data = await self.http_client.get(url)
            results = data.get("results", [])
            total = data.get("count", 0)

            entities = [self.entity_class(**item) for item in results]

            if sort_by:
                entities = self._sort_entities(entities, sort_by, sort_order)

            if filters:
                entities = self._filter_entities(entities, filters)

            if settings.CACHE_ENABLED:
                cache_data = {
                    "items": [entity.dict() for entity in entities],
                    "total": total,
                }
                await self.cache.set(cache_key, cache_data, settings.CACHE_TTL)

            return entities, total
        except Exception as e:
            logger.error(f"Erro ao obter todos os {self.resource_type}: {str(e)}")
            return [], 0

    async def search(self, query: str) -> List[T]:
        """Busca recursos por query."""
        cache_key = self._get_cache_key("search", query)

        if settings.CACHE_ENABLED:
            cached = await self.cache.get(cache_key)
            if cached:
                logger.debug(f"Cache hit para {cache_key}")
                return [self.entity_class(**item) for item in cached]

        try:
            url = self._build_url()
            params = {"search": query}

            data = await self.http_client.get(url)
            results = data.get("results", [])
            entities = [self.entity_class(**item) for item in results]

            if settings.CACHE_ENABLED:
                await self.cache.set(
                    cache_key,
                    [entity.dict() for entity in entities],
                    settings.CACHE_TTL,
                )

            return entities
        except Exception as e:
            logger.error(f"Erro ao buscar {self.resource_type} com query '{query}': {str(e)}")
            return []

    async def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Conta o número de recursos."""
        try:
            url = self._build_url()
            data = await self.http_client.get(url)
            return data.get("count", 0)
        except Exception as e:
            logger.error(f"Erro ao contar {self.resource_type}: {str(e)}")
            return 0

    def _filter_entities(
        self, entities: List[T], filters: Dict[str, Any]
    ) -> List[T]:
        """Filtra entidades baseado em critérios."""
        filtered = entities

        for field, value in filters.items():
            if not hasattr(filtered[0] if filtered else None, field):
                raise InvalidFilterError(field, f"Campo '{field}' não existe")

            filtered = [
                entity
                for entity in filtered
                if self._match_filter(getattr(entity, field), value)
            ]

        return filtered

    def _match_filter(self, field_value: Any, filter_value: Any) -> bool:
        """Verifica se um valor corresponde ao filtro."""
        if isinstance(filter_value, dict):
            operator = filter_value.get("operator", "eq")
            value = filter_value.get("value")

            if operator == "eq":
                return field_value == value
            elif operator == "ne":
                return field_value != value
            elif operator == "contains":
                return str(value).lower() in str(field_value).lower()
            elif operator == "in":
                return field_value in value
            else:
                return False

        return field_value == filter_value

    def _sort_entities(
        self, entities: List[T], sort_by: str, sort_order: str = "asc"
    ) -> List[T]:
        """Ordena entidades."""
        if not entities:
            return entities

        if not hasattr(entities[0], sort_by):
            raise InvalidFilterError(sort_by, f"Campo '{sort_by}' não existe")

        reverse = sort_order.lower() == "desc"
        return sorted(entities, key=lambda x: getattr(x, sort_by), reverse=reverse)
