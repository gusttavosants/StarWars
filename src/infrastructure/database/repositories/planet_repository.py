from src.infrastructure.database.repositories.base_repository import BaseRepository
from src.domain.entities.planet import Planet
from src.domain.interfaces.client import IHttpClient
from src.domain.interfaces.cache import ICache


class PlanetRepository(BaseRepository[Planet]):
    """Repositório para planetas."""

    def __init__(self, http_client: IHttpClient, cache: ICache):
        super().__init__(
            http_client=http_client,
            cache=cache,
            resource_type="planets",
            entity_class=Planet,
        )
