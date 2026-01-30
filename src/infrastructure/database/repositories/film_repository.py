from src.infrastructure.database.repositories.base_repository import BaseRepository
from src.domain.entities.film import Film
from src.domain.interfaces.client import IHttpClient
from src.domain.interfaces.cache import ICache


class FilmRepository(BaseRepository[Film]):
    """Repositório para filmes."""

    def __init__(self, http_client: IHttpClient, cache: ICache):
        super().__init__(
            http_client=http_client,
            cache=cache,
            resource_type="films",
            entity_class=Film,
        )
