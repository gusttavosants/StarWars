import logging
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from src.application.services.analytics_service import AnalyticsService
from src.application.security.auth import get_optional_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])

analytics_service = AnalyticsService()


@router.get(
    "/performance",
    summary="Métricas de Performance",
    description="Obtém métricas gerais de performance da API",
)
async def get_performance_metrics(
    current_user: Optional[str] = Depends(get_optional_user),
):
    """Retorna métricas de performance da API."""
    try:
        metrics = await analytics_service.get_performance_metrics()
        return metrics
    except Exception as e:
        logger.error(f"Erro ao obter métricas: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter métricas",
        )


@router.get(
    "/endpoints/top",
    summary="Endpoints Mais Acessados",
    description="Obtém os endpoints mais acessados",
)
async def get_top_endpoints(
    limit: int = 10,
    current_user: Optional[str] = Depends(get_optional_user),
):
    """Retorna endpoints mais acessados."""
    try:
        endpoints = await analytics_service.get_top_endpoints(limit)
        return {"endpoints": endpoints}
    except Exception as e:
        logger.error(f"Erro ao obter endpoints: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter endpoints",
        )


@router.get(
    "/users/top",
    summary="Usuários Mais Ativos",
    description="Obtém os usuários mais ativos",
)
async def get_top_users(
    limit: int = 10,
    current_user: Optional[str] = Depends(get_optional_user),
):
    """Retorna usuários mais ativos."""
    try:
        users = await analytics_service.get_top_users(limit)
        return {"users": users}
    except Exception as e:
        logger.error(f"Erro ao obter usuários: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter usuários",
        )


@router.get(
    "/hourly",
    summary="Estatísticas por Hora",
    description="Obtém estatísticas de requisições por hora",
)
async def get_hourly_stats(
    current_user: Optional[str] = Depends(get_optional_user),
):
    """Retorna estatísticas por hora."""
    try:
        stats = await analytics_service.get_hourly_stats()
        return stats
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter estatísticas",
        )
