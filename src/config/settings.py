import os
from typing import Optional


class Settings:
    """Configurações da aplicação baseadas em variáveis de ambiente."""

    # Aplicação
    APP_NAME: str = "Star Wars API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # API SWAPI
    SWAPI_BASE_URL: str = "https://swapi.dev/api"
    SWAPI_TIMEOUT: int = int(os.getenv("SWAPI_TIMEOUT", "10"))

    # Cache
    CACHE_ENABLED: bool = os.getenv("CACHE_ENABLED", "True").lower() == "true"
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "3600"))
    REDIS_URL: Optional[str] = os.getenv("REDIS_URL")

    # JWT
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = os.getenv("RATE_LIMIT_ENABLED", "True").lower() == "true"
    RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    RATE_LIMIT_PERIOD: int = int(os.getenv("RATE_LIMIT_PERIOD", "3600"))

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # GCP
    GCP_PROJECT_ID: Optional[str] = os.getenv("GCP_PROJECT_ID")
    GCP_ENVIRONMENT: str = os.getenv("GCP_ENVIRONMENT", "local")

    @classmethod
    def is_production(cls) -> bool:
        """Verifica se está em ambiente de produção."""
        return cls.ENVIRONMENT == "production"

    @classmethod
    def is_development(cls) -> bool:
        """Verifica se está em ambiente de desenvolvimento."""
        return cls.ENVIRONMENT == "development"


settings = Settings()
