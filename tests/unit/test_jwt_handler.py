from datetime import datetime, timedelta

import pytest

from src.application.security.jwt_handler import JWTHandler
from src.config.exceptions import InvalidTokenError


class TestJWTHandler:
    """Testes para JWT Handler."""

    def test_create_token_success(self):
        """Testa criação de token com sucesso."""
        data = {"sub": "testuser"}
        token = JWTHandler.create_token(data)

        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_token_with_custom_expiration(self):
        """Testa criação de token com expiração customizada."""
        data = {"sub": "testuser"}
        expires_delta = timedelta(hours=1)
        token = JWTHandler.create_token(data, expires_delta)

        assert token is not None
        payload = JWTHandler.verify_token(token)
        assert payload["sub"] == "testuser"

    def test_verify_token_success(self):
        """Testa verificação de token válido."""
        data = {"sub": "testuser", "role": "admin"}
        token = JWTHandler.create_token(data)

        payload = JWTHandler.verify_token(token)

        assert payload["sub"] == "testuser"
        assert payload["role"] == "admin"
        assert "exp" in payload

    def test_verify_token_invalid(self):
        """Testa verificação de token inválido."""
        invalid_token = "invalid.token.here"

        with pytest.raises(InvalidTokenError):
            JWTHandler.verify_token(invalid_token)

    def test_verify_token_malformed(self):
        """Testa verificação de token malformado."""
        malformed_token = "not_a_valid_jwt"

        with pytest.raises(InvalidTokenError):
            JWTHandler.verify_token(malformed_token)

    def test_get_username_from_token_success(self):
        """Testa extração de username de token válido."""
        data = {"sub": "luke_skywalker"}
        token = JWTHandler.create_token(data)

        username = JWTHandler.get_username_from_token(token)

        assert username == "luke_skywalker"

    def test_get_username_from_token_invalid(self):
        """Testa extração de username de token inválido."""
        invalid_token = "invalid.token.here"

        with pytest.raises(InvalidTokenError):
            JWTHandler.get_username_from_token(invalid_token)

    def test_get_username_from_token_no_sub(self):
        """Testa extração de username quando token não tem 'sub'."""
        data = {"role": "admin"}
        token = JWTHandler.create_token(data)

        with pytest.raises(InvalidTokenError):
            JWTHandler.get_username_from_token(token)

    def test_token_contains_exp(self):
        """Testa se token contém campo de expiração."""
        data = {"sub": "testuser"}
        token = JWTHandler.create_token(data)

        payload = JWTHandler.verify_token(token)

        assert "exp" in payload
        assert isinstance(payload["exp"], int)

    def test_token_expiration_in_future(self):
        """Testa se expiração do token está no futuro."""
        data = {"sub": "testuser"}
        token = JWTHandler.create_token(data)

        payload = JWTHandler.verify_token(token)
        exp_time = datetime.fromtimestamp(payload["exp"])

        assert exp_time > datetime.utcnow()

    def test_create_token_with_multiple_claims(self):
        """Testa criação de token com múltiplas claims."""
        data = {
            "sub": "testuser",
            "role": "admin",
            "permissions": ["read", "write"],
            "org_id": "org123",
        }
        token = JWTHandler.create_token(data)

        payload = JWTHandler.verify_token(token)

        assert payload["sub"] == "testuser"
        assert payload["role"] == "admin"
        assert payload["permissions"] == ["read", "write"]
        assert payload["org_id"] == "org123"
