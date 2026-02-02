import logging
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from src.application.security.jwt_handler import JWTHandler
from src.config.exceptions import InvalidTokenError

logger = logging.getLogger(__name__)

security = HTTPBearer()


async def get_current_user(
    credentials = Depends(security),
) -> str:
    """Obtém o usuário atual a partir do token JWT."""
    token = credentials.credentials

    try:
        username = JWTHandler.get_username_from_token(token)
        return username
    except InvalidTokenError as e:
        logger.warning(f"Tentativa de acesso com token inválido: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logger.error(f"Erro ao autenticar usuário: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Erro ao autenticar",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_optional_user(
    credentials: Optional[object] = Depends(security),
) -> Optional[str]:
    """Obtém o usuário atual de forma opcional."""
    if not credentials:
        return None

    try:
        username = JWTHandler.get_username_from_token(credentials.credentials)
        return username
    except Exception:
        return None
