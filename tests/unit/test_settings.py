import pytest

from src.config.settings import Settings


class TestSettings:
    """Testes para configurações da aplicação."""

    def test_settings_creation(self):
        """Testa criação de settings."""
        settings = Settings()

        assert settings.APP_NAME == "Star Wars API"
        assert settings.APP_VERSION == "1.0.0"

    def test_settings_swapi_base_url(self):
        """Testa URL base da SWAPI."""
        settings = Settings()
        assert settings.SWAPI_BASE_URL == "https://swapi.dev/api"

    def test_settings_swapi_timeout_default(self):
        """Testa timeout padrão da SWAPI."""
        settings = Settings()
        assert settings.SWAPI_TIMEOUT == 10
        assert isinstance(settings.SWAPI_TIMEOUT, int)

    def test_settings_cache_ttl_default(self):
        """Testa TTL padrão do cache."""
        settings = Settings()
        assert settings.CACHE_TTL == 3600
        assert isinstance(settings.CACHE_TTL, int)

    def test_settings_jwt_secret_key_default(self):
        """Testa chave secreta JWT padrão."""
        settings = Settings()
        assert settings.JWT_SECRET_KEY is not None
        assert len(settings.JWT_SECRET_KEY) > 0

    def test_settings_jwt_algorithm(self):
        """Testa algoritmo JWT."""
        settings = Settings()
        assert settings.JWT_ALGORITHM == "HS256"

    def test_settings_jwt_expiration_hours_default(self):
        """Testa horas de expiração JWT padrão."""
        settings = Settings()
        assert settings.JWT_EXPIRATION_HOURS == 24
        assert isinstance(settings.JWT_EXPIRATION_HOURS, int)

    def test_settings_rate_limit_requests_default(self):
        """Testa limite de requisições padrão."""
        settings = Settings()
        assert settings.RATE_LIMIT_REQUESTS == 100
        assert isinstance(settings.RATE_LIMIT_REQUESTS, int)

    def test_settings_rate_limit_period_default(self):
        """Testa período de rate limiting padrão."""
        settings = Settings()
        assert settings.RATE_LIMIT_PERIOD == 3600
        assert isinstance(settings.RATE_LIMIT_PERIOD, int)

    def test_settings_log_level_default(self):
        """Testa nível de logging padrão."""
        settings = Settings()
        assert settings.LOG_LEVEL == "INFO"

    def test_settings_gcp_environment_default(self):
        """Testa ambiente GCP padrão."""
        settings = Settings()
        assert settings.GCP_ENVIRONMENT == "local"

    def test_settings_all_attributes_exist(self):
        """Testa que todos os atributos existem."""
        settings = Settings()

        required_attributes = [
            "APP_NAME",
            "APP_VERSION",
            "DEBUG",
            "ENVIRONMENT",
            "SWAPI_BASE_URL",
            "SWAPI_TIMEOUT",
            "CACHE_ENABLED",
            "CACHE_TTL",
            "REDIS_URL",
            "JWT_SECRET_KEY",
            "JWT_ALGORITHM",
            "JWT_EXPIRATION_HOURS",
            "RATE_LIMIT_ENABLED",
            "RATE_LIMIT_REQUESTS",
            "RATE_LIMIT_PERIOD",
            "LOG_LEVEL",
            "GCP_PROJECT_ID",
            "GCP_ENVIRONMENT",
        ]

        for attr in required_attributes:
            assert hasattr(settings, attr)

    def test_settings_singleton_instance(self):
        """Testa que settings é uma instância única."""
        from src.config.settings import settings as settings_instance

        assert settings_instance is not None
        assert isinstance(settings_instance, Settings)

    def test_settings_is_production_method_exists(self):
        """Testa que método is_production existe."""
        assert hasattr(Settings, "is_production")
        assert callable(Settings.is_production)

    def test_settings_is_development_method_exists(self):
        """Testa que método is_development existe."""
        assert hasattr(Settings, "is_development")
        assert callable(Settings.is_development)
