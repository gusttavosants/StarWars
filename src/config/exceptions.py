"""Exceções customizadas da aplicação."""


class StarWarsAPIException(Exception):
    """Exceção base da aplicação."""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ResourceNotFoundError(StarWarsAPIException):
    """Exceção lançada quando um recurso não é encontrado."""

    def __init__(self, resource_type: str, resource_id: str):
        message = f"{resource_type} com ID '{resource_id}' não encontrado"
        super().__init__(message, status_code=404)


class InvalidFilterError(StarWarsAPIException):
    """Exceção lançada quando um filtro é inválido."""

    def __init__(self, filter_name: str, reason: str):
        message = f"Filtro inválido '{filter_name}': {reason}"
        super().__init__(message, status_code=400)


class InvalidSortError(StarWarsAPIException):
    """Exceção lançada quando uma ordenação é inválida."""

    def __init__(self, sort_field: str, reason: str):
        message = f"Ordenação inválida '{sort_field}': {reason}"
        super().__init__(message, status_code=400)


class UnauthorizedError(StarWarsAPIException):
    """Exceção lançada quando o usuário não está autorizado."""

    def __init__(self, message: str = "Não autorizado"):
        super().__init__(message, status_code=401)


class InvalidTokenError(StarWarsAPIException):
    """Exceção lançada quando o token é inválido."""

    def __init__(self, message: str = "Token inválido"):
        super().__init__(message, status_code=401)


class ExpiredTokenError(StarWarsAPIException):
    """Exceção lançada quando o token expirou."""

    def __init__(self, message: str = "Token expirado"):
        super().__init__(message, status_code=401)


class RateLimitExceededError(StarWarsAPIException):
    """Exceção lançada quando o limite de requisições é excedido."""

    def __init__(self, message: str = "Limite de requisições excedido"):
        super().__init__(message, status_code=429)


class ExternalAPIError(StarWarsAPIException):
    """Exceção lançada quando há erro na API externa (SWAPI)."""

    def __init__(self, message: str, status_code: int = 502):
        super().__init__(message, status_code=status_code)


class CacheError(StarWarsAPIException):
    """Exceção lançada quando há erro no cache."""

    def __init__(self, message: str):
        super().__init__(message, status_code=500)
