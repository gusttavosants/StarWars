import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from src.config.settings import settings
from src.config.exceptions import InvalidTokenError, ExpiredTokenError

logger = logging.getLogger(__name__)


class JWTHandler:
    """Handler para gerenciar JWT tokens."""

    @staticmethod
    def create_token(
        data: Dict[str, Any],
        expires_delta: Optional[timedelta] = None,
    ) -> str:
        """Cria um JWT token."""
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                hours=settings.JWT_EXPIRATION_HOURS
            )

        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(
            to_encode,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )

        logger.debug(f"Token criado para usuário: {data.get('sub')}")
        return encoded_jwt

    @staticmethod
    def verify_token(token: str) -> Dict[str, Any]:
        """Verifica e decodifica um JWT token."""
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
            return payload
        except JWTError as e:
            logger.error(f"Erro ao verificar token: {str(e)}")
            raise InvalidTokenError("Token inválido ou expirado")
        except Exception as e:
            logger.error(f"Erro inesperado ao verificar token: {str(e)}")
            raise InvalidTokenError("Erro ao verificar token")

    @staticmethod
    def get_username_from_token(token: str) -> Optional[str]:
        """Extrai o nome de usuário de um token."""
        try:
            payload = JWTHandler.verify_token(token)
            username: str = payload.get("sub")
            if username is None:
                raise InvalidTokenError("Token sem usuário")
            return username
        except InvalidTokenError:
            raise
        except Exception as e:
            logger.error(f"Erro ao extrair usuário do token: {str(e)}")
            raise InvalidTokenError("Erro ao extrair usuário do token")
