import pytest

from src.config.exceptions import (
    CacheError,
    ExpiredTokenError,
    ExternalAPIError,
    InvalidFilterError,
    InvalidSortError,
    InvalidTokenError,
    RateLimitExceededError,
    ResourceNotFoundError,
    StarWarsAPIException,
    UnauthorizedError,
)


class TestStarWarsAPIException:
    """Testes para exceção base."""

    def test_base_exception_creation(self):
        """Testa criação de exceção base."""
        exc = StarWarsAPIException("Test error", 500)

        assert exc.message == "Test error"
        assert exc.status_code == 500

    def test_base_exception_default_status_code(self):
        """Testa código de status padrão."""
        exc = StarWarsAPIException("Test error")

        assert exc.status_code == 500

    def test_base_exception_str_representation(self):
        """Testa representação em string."""
        exc = StarWarsAPIException("Test error", 500)

        assert str(exc) == "Test error"


class TestResourceNotFoundError:
    """Testes para ResourceNotFoundError."""

    def test_resource_not_found_creation(self):
        """Testa criação de exceção."""
        exc = ResourceNotFoundError("Character", "1")

        assert "Character" in exc.message
        assert "1" in exc.message
        assert exc.status_code == 404

    def test_resource_not_found_different_types(self):
        """Testa com diferentes tipos de recursos."""
        resources = ["Character", "Planet", "Starship", "Film"]

        for resource in resources:
            exc = ResourceNotFoundError(resource, "123")
            assert resource in exc.message
            assert exc.status_code == 404

    def test_resource_not_found_message_format(self):
        """Testa formato da mensagem."""
        exc = ResourceNotFoundError("Character", "999")

        assert "não encontrado" in exc.message.lower()


class TestInvalidFilterError:
    """Testes para InvalidFilterError."""

    def test_invalid_filter_creation(self):
        """Testa criação de exceção."""
        exc = InvalidFilterError("gender", "Campo inválido")

        assert "gender" in exc.message
        assert "Campo inválido" in exc.message
        assert exc.status_code == 400

    def test_invalid_filter_different_fields(self):
        """Testa com diferentes campos."""
        fields = ["gender", "height", "invalid_field"]

        for field in fields:
            exc = InvalidFilterError(field, "Motivo do erro")
            assert field in exc.message
            assert exc.status_code == 400


class TestInvalidSortError:
    """Testes para InvalidSortError."""

    def test_invalid_sort_creation(self):
        """Testa criação de exceção."""
        exc = InvalidSortError("invalid_field", "Campo não existe")

        assert "invalid_field" in exc.message
        assert "Campo não existe" in exc.message
        assert exc.status_code == 400

    def test_invalid_sort_different_fields(self):
        """Testa com diferentes campos."""
        fields = ["name", "height", "invalid_field"]

        for field in fields:
            exc = InvalidSortError(field, "Motivo")
            assert field in exc.message
            assert exc.status_code == 400


class TestUnauthorizedError:
    """Testes para UnauthorizedError."""

    def test_unauthorized_creation(self):
        """Testa criação de exceção."""
        exc = UnauthorizedError()

        assert exc.status_code == 401
        assert "Não autorizado" in exc.message

    def test_unauthorized_custom_message(self):
        """Testa com mensagem customizada."""
        exc = UnauthorizedError("Acesso negado")

        assert exc.message == "Acesso negado"
        assert exc.status_code == 401


class TestInvalidTokenError:
    """Testes para InvalidTokenError."""

    def test_invalid_token_creation(self):
        """Testa criação de exceção."""
        exc = InvalidTokenError()

        assert exc.status_code == 401
        assert "Token" in exc.message

    def test_invalid_token_custom_message(self):
        """Testa com mensagem customizada."""
        exc = InvalidTokenError("Token expirado")

        assert exc.message == "Token expirado"
        assert exc.status_code == 401


class TestExpiredTokenError:
    """Testes para ExpiredTokenError."""

    def test_expired_token_creation(self):
        """Testa criação de exceção."""
        exc = ExpiredTokenError()

        assert exc.status_code == 401
        assert "Token" in exc.message

    def test_expired_token_custom_message(self):
        """Testa com mensagem customizada."""
        exc = ExpiredTokenError("Token expirou em 2024-01-30")

        assert exc.message == "Token expirou em 2024-01-30"
        assert exc.status_code == 401


class TestRateLimitExceededError:
    """Testes para RateLimitExceededError."""

    def test_rate_limit_exceeded_creation(self):
        """Testa criação de exceção."""
        exc = RateLimitExceededError()

        assert exc.status_code == 429
        assert "Limite" in exc.message

    def test_rate_limit_exceeded_custom_message(self):
        """Testa com mensagem customizada."""
        exc = RateLimitExceededError("Limite de 100 requisições por hora excedido")

        assert exc.message == "Limite de 100 requisições por hora excedido"
        assert exc.status_code == 429


class TestExternalAPIError:
    """Testes para ExternalAPIError."""

    def test_external_api_error_creation(self):
        """Testa criação de exceção."""
        exc = ExternalAPIError("SWAPI indisponível")

        assert exc.message == "SWAPI indisponível"
        assert exc.status_code == 502

    def test_external_api_error_custom_status_code(self):
        """Testa com código de status customizado."""
        exc = ExternalAPIError("Erro 503", 503)

        assert exc.message == "Erro 503"
        assert exc.status_code == 503

    def test_external_api_error_different_status_codes(self):
        """Testa com diferentes códigos de status."""
        status_codes = [502, 503, 504]

        for code in status_codes:
            exc = ExternalAPIError("Erro", code)
            assert exc.status_code == code


class TestCacheError:
    """Testes para CacheError."""

    def test_cache_error_creation(self):
        """Testa criação de exceção."""
        exc = CacheError("Erro ao conectar ao Redis")

        assert exc.message == "Erro ao conectar ao Redis"
        assert exc.status_code == 500

    def test_cache_error_different_messages(self):
        """Testa com diferentes mensagens."""
        messages = [
            "Erro ao conectar ao Redis",
            "Erro ao obter chave do cache",
            "Erro ao definir chave no cache",
            "Erro ao limpar cache",
        ]

        for msg in messages:
            exc = CacheError(msg)
            assert exc.message == msg
            assert exc.status_code == 500


class TestExceptionHierarchy:
    """Testes para hierarquia de exceções."""

    def test_all_exceptions_inherit_from_base(self):
        """Testa que todas as exceções herdam da base."""
        exceptions = [
            ResourceNotFoundError("Test", "1"),
            InvalidFilterError("field", "reason"),
            InvalidSortError("field", "reason"),
            UnauthorizedError(),
            InvalidTokenError(),
            ExpiredTokenError(),
            RateLimitExceededError(),
            ExternalAPIError("error"),
            CacheError("error"),
        ]

        for exc in exceptions:
            assert isinstance(exc, StarWarsAPIException)

    def test_exception_status_codes(self):
        """Testa códigos de status das exceções."""
        assert ResourceNotFoundError("Test", "1").status_code == 404
        assert InvalidFilterError("field", "reason").status_code == 400
        assert InvalidSortError("field", "reason").status_code == 400
        assert UnauthorizedError().status_code == 401
        assert InvalidTokenError().status_code == 401
        assert ExpiredTokenError().status_code == 401
        assert RateLimitExceededError().status_code == 429
        assert ExternalAPIError("error").status_code == 502
        assert CacheError("error").status_code == 500

    def test_exception_messages_not_empty(self):
        """Testa que mensagens não estão vazias."""
        exceptions = [
            ResourceNotFoundError("Test", "1"),
            InvalidFilterError("field", "reason"),
            InvalidSortError("field", "reason"),
            UnauthorizedError(),
            InvalidTokenError(),
            ExpiredTokenError(),
            RateLimitExceededError(),
            ExternalAPIError("error"),
            CacheError("error"),
        ]

        for exc in exceptions:
            assert len(exc.message) > 0
            assert isinstance(exc.message, str)


class TestExceptionUsage:
    """Testes para uso prático de exceções."""

    def test_exception_can_be_raised(self):
        """Testa que exceções podem ser lançadas."""
        with pytest.raises(ResourceNotFoundError):
            raise ResourceNotFoundError("Character", "1")

    def test_exception_can_be_caught(self):
        """Testa que exceções podem ser capturadas."""
        try:
            raise InvalidFilterError("field", "reason")
        except StarWarsAPIException as e:
            assert e.status_code == 400

    def test_multiple_exception_handling(self):
        """Testa tratamento de múltiplas exceções."""
        exceptions_to_test = [
            (ResourceNotFoundError("Test", "1"), 404),
            (UnauthorizedError(), 401),
            (RateLimitExceededError(), 429),
        ]

        for exc, expected_code in exceptions_to_test:
            try:
                raise exc
            except StarWarsAPIException as e:
                assert e.status_code == expected_code
