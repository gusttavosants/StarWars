"""Constantes da aplicação Star Wars API."""

# Tipos de recursos SWAPI
RESOURCE_TYPES = {
    "characters": "people",
    "planets": "planets",
    "starships": "starships",
    "films": "films",
}

# Campos padrão para cada recurso
CHARACTER_FIELDS = [
    "name",
    "height",
    "mass",
    "hair_color",
    "skin_color",
    "eye_color",
    "birth_year",
    "gender",
    "homeworld",
    "films",
    "species",
    "vehicles",
    "starships",
]

PLANET_FIELDS = [
    "name",
    "rotation_period",
    "orbital_period",
    "diameter",
    "climate",
    "gravity",
    "terrain",
    "surface_water",
    "population",
    "residents",
    "films",
]

STARSHIP_FIELDS = [
    "name",
    "model",
    "manufacturer",
    "cost_in_credits",
    "length",
    "max_atmosphering_speed",
    "crew",
    "passengers",
    "cargo_capacity",
    "consumables",
    "hyperdrive_rating",
    "MGLT",
    "starship_class",
    "pilots",
    "films",
]

FILM_FIELDS = [
    "title",
    "episode_id",
    "opening_crawl",
    "director",
    "producer",
    "release_date",
    "characters",
    "planets",
    "starships",
    "vehicles",
    "species",
]

# Operadores de filtro suportados
FILTER_OPERATORS = {
    "eq": "equals",
    "ne": "not equals",
    "gt": "greater than",
    "gte": "greater than or equals",
    "lt": "less than",
    "lte": "less than or equals",
    "contains": "contains substring",
    "in": "in list",
}

# Ordenação padrão
SORT_ORDERS = ["asc", "desc"]
DEFAULT_SORT_ORDER = "asc"

# Paginação
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100

# Mensagens de erro
ERROR_MESSAGES = {
    "resource_not_found": "Recurso não encontrado",
    "invalid_filter": "Filtro inválido",
    "invalid_sort": "Ordenação inválida",
    "unauthorized": "Não autorizado",
    "invalid_token": "Token inválido",
    "expired_token": "Token expirado",
    "rate_limit_exceeded": "Limite de requisições excedido",
    "internal_error": "Erro interno do servidor",
}

# Cache keys
CACHE_KEY_CHARACTERS = "characters:{}"
CACHE_KEY_PLANETS = "planets:{}"
CACHE_KEY_STARSHIPS = "starships:{}"
CACHE_KEY_FILMS = "films:{}"
CACHE_KEY_CHARACTER_BY_ID = "character:{}:{}"
CACHE_KEY_PLANET_BY_ID = "planet:{}:{}"
CACHE_KEY_STARSHIP_BY_ID = "starship:{}:{}"
CACHE_KEY_FILM_BY_ID = "film:{}:{}"
