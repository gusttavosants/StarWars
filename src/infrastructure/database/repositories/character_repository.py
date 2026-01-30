from src.infrastructure.database.repositories.base_repository import BaseRepository
from src.domain.entities.character import Character
from src.domain.interfaces.client import IHttpClient
from src.domain.interfaces.cache import ICache


class CharacterRepository(BaseRepository[Character]):
    """Repositório para personagens."""

    def __init__(self, http_client: IHttpClient, cache: ICache):
        super().__init__(
            http_client=http_client,
            cache=cache,
            resource_type="people",
            entity_class=Character,
        )
