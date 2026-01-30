import logging
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from src.application.services.audit_service import AuditService, AuditEventType
from src.application.security.auth import get_optional_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/audit", tags=["Audit"])

audit_service = AuditService()


@router.get(
    "/summary",
    summary="Resumo de Auditoria",
    description="Obtém resumo geral de eventos de auditoria",
)
async def get_audit_summary(
    current_user: Optional[str] = Depends(get_optional_user),
):
    """Retorna resumo de eventos de auditoria."""
    try:
        summary = await audit_service.get_event_summary()
        return summary
    except Exception as e:
        logger.error(f"Erro ao obter resumo: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter resumo",
        )


@router.get(
    "/user/{user_id}",
    summary="Histórico de Usuário",
    description="Obtém histórico de auditoria de um usuário",
)
async def get_user_audit_trail(
    user_id: str,
    days: int = 7,
    current_user: Optional[str] = Depends(get_optional_user),
):
    """Retorna histórico de auditoria de um usuário."""
    try:
        trail = await audit_service.get_user_audit_trail(user_id, days)
        return {
            "user_id": user_id,
            "days": days,
            "events": trail,
            "total_events": len(trail),
        }
    except Exception as e:
        logger.error(f"Erro ao obter histórico: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter histórico",
        )


@router.get(
    "/suspicious",
    summary="Atividades Suspeitas",
    description="Identifica atividades suspeitas",
)
async def get_suspicious_activities(
    current_user: Optional[str] = Depends(get_optional_user),
):
    """Retorna atividades suspeitas."""
    try:
        suspicious = await audit_service.get_suspicious_activities()
        return {
            "suspicious_activities": suspicious,
            "total": len(suspicious),
        }
    except Exception as e:
        logger.error(f"Erro ao obter atividades suspeitas: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter atividades suspeitas",
        )


@router.get(
    "/ip/{ip_address}",
    summary="Atividade por IP",
    description="Obtém atividade de um endereço IP",
)
async def get_ip_activity(
    ip_address: str,
    current_user: Optional[str] = Depends(get_optional_user),
):
    """Retorna atividade de um IP."""
    try:
        activity = await audit_service.get_ip_activity(ip_address)
        return activity
    except Exception as e:
        logger.error(f"Erro ao obter atividade do IP: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter atividade do IP",
        )


@router.get(
    "/security-alerts",
    summary="Alertas de Segurança",
    description="Obtém alertas de segurança recentes",
)
async def get_security_alerts(
    current_user: Optional[str] = Depends(get_optional_user),
):
    """Retorna alertas de segurança recentes."""
    try:
        summary = await audit_service.get_event_summary()
        return {
            "total_alerts": summary["total_security_alerts"],
            "recent_alerts": summary["recent_alerts"],
        }
    except Exception as e:
        logger.error(f"Erro ao obter alertas: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter alertas",
        )
