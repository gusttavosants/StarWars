from src.infrastructure.database.repositories.base_repository import BaseRepository
from src.domain.entities.starship import Starship
from src.domain.interfaces.client import IHttpClient
from src.domain.interfaces.cache import ICache


class StarshipRepository(BaseRepository[Starship]):
    """Repositório para naves estelares."""

    def __init__(self, http_client: IHttpClient, cache: ICache):
        super().__init__(
            http_client=http_client,
            cache=cache,
            resource_type="starships",
            entity_class=Starship,
        )
