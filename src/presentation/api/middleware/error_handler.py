import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from src.config.exceptions import StarWarsAPIException
from src.application.dto.filters import ErrorResponse

logger = logging.getLogger(__name__)


async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handler genérico para exceções."""
    if isinstance(exc, StarWarsAPIException):
        logger.warning(f"Erro esperado: {exc.message}")
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                error=exc.__class__.__name__,
                message=exc.message,
                status_code=exc.status_code,
            ).dict(),
        )

    logger.error(f"Erro não tratado: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="InternalServerError",
            message="Erro interno do servidor",
            status_code=500,
        ).dict(),
    )
