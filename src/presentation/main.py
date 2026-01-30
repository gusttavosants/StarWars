from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.config.settings import settings
from src.config.exceptions import StarWarsAPIException
from src.application.dto.filters import ErrorResponse
from src.presentation.api.routes import characters, planets, starships, films
import logging

logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Factory function para criar a aplicação FastAPI."""
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="API para explorar dados de Star Wars",
        debug=settings.DEBUG,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    add_middleware(app)
    add_routes(app)
    add_exception_handlers(app)

    @app.on_event("startup")
    async def startup_event():
        logger.info(f"Iniciando {settings.APP_NAME} v{settings.APP_VERSION}")
        logger.info(f"Ambiente: {settings.ENVIRONMENT}")

    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info(f"Encerrando {settings.APP_NAME}")

    @app.get("/health", tags=["Health"])
    async def health_check():
        """Verifica a saúde da aplicação."""
        return {
            "status": "healthy",
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION,
        }

    return app


def add_middleware(app: FastAPI) -> None:
    """Adiciona middlewares à aplicação."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def add_routes(app: FastAPI) -> None:
    """Adiciona rotas à aplicação."""
    @app.get("/", tags=["Root"])
    async def root():
        return {
            "message": "Bem-vindo à Star Wars API",
            "version": settings.APP_VERSION,
            "docs": "/docs",
            "endpoints": {
                "characters": "/api/characters",
                "planets": "/api/planets",
                "starships": "/api/starships",
                "films": "/api/films",
            },
        }

    app.include_router(characters.router)
    app.include_router(planets.router)
    app.include_router(starships.router)
    app.include_router(films.router)


def add_exception_handlers(app: FastAPI) -> None:
    """Adiciona handlers de exceção à aplicação."""
    @app.exception_handler(StarWarsAPIException)
    async def starwars_exception_handler(request: Request, exc: StarWarsAPIException):
        logger.warning(f"Erro esperado: {exc.message}")
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                error=exc.__class__.__name__,
                message=exc.message,
                status_code=exc.status_code,
            ).dict(),
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"Erro não tratado: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                error="InternalServerError",
                message="Erro interno do servidor",
                status_code=500,
            ).dict(),
        )


app = create_app()
