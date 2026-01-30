import logging
from typing import Dict, List, Any
from datetime import datetime, timedelta
from enum import Enum
from collections import defaultdict

logger = logging.getLogger(__name__)


class AuditEventType(str, Enum):
    """Tipos de eventos de auditoria."""
    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    API_REQUEST = "api_request"
    API_ERROR = "api_error"
    RESOURCE_ACCESSED = "resource_accessed"
    RESOURCE_MODIFIED = "resource_modified"
    AUTHENTICATION_FAILED = "authentication_failed"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    SECURITY_ALERT = "security_alert"


class AuditService:
    """Serviço de auditoria e logging avançado."""

    def __init__(self):
        self.audit_log: List[Dict[str, Any]] = []
        self.event_counts: Dict[str, int] = defaultdict(int)
        self.user_activities: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.security_alerts: List[Dict[str, Any]] = []

    async def log_event(
        self,
        event_type: AuditEventType,
        user_id: str,
        resource_type: str = None,
        resource_id: str = None,
        details: Dict[str, Any] = None,
        ip_address: str = None,
        status_code: int = None,
    ) -> None:
        """Registra um evento de auditoria."""
        event = {
            "timestamp": datetime.utcnow(),
            "event_type": event_type.value,
            "user_id": user_id,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "details": details or {},
            "ip_address": ip_address,
            "status_code": status_code,
        }

        self.audit_log.append(event)
        self.event_counts[event_type.value] += 1
        self.user_activities[user_id].append(event)

        logger.info(f"Audit event: {event_type.value} by {user_id}")

    async def log_api_request(
        self,
        user_id: str,
        endpoint: str,
        method: str,
        status_code: int,
        response_time: float,
        ip_address: str = None,
    ) -> None:
        """Registra uma requisição de API."""
        await self.log_event(
            AuditEventType.API_REQUEST,
            user_id,
            resource_type="api",
            details={
                "endpoint": endpoint,
                "method": method,
                "response_time_ms": response_time,
            },
            ip_address=ip_address,
            status_code=status_code,
        )

    async def log_authentication_failure(
        self,
        user_id: str,
        reason: str,
        ip_address: str = None,
    ) -> None:
        """Registra falha de autenticação."""
        await self.log_event(
            AuditEventType.AUTHENTICATION_FAILED,
            user_id,
            details={"reason": reason},
            ip_address=ip_address,
        )

        # Verificar padrão suspeito (múltiplas falhas)
        recent_failures = [
            e for e in self.user_activities[user_id]
            if e["event_type"] == AuditEventType.AUTHENTICATION_FAILED.value
            and (datetime.utcnow() - e["timestamp"]).total_seconds() < 300
        ]

        if len(recent_failures) >= 3:
            await self.log_security_alert(
                user_id,
                "Multiple authentication failures",
                {"failures_count": len(recent_failures)},
                ip_address,
            )

    async def log_security_alert(
        self,
        user_id: str,
        alert_type: str,
        details: Dict[str, Any] = None,
        ip_address: str = None,
    ) -> None:
        """Registra um alerta de segurança."""
        alert = {
            "timestamp": datetime.utcnow(),
            "user_id": user_id,
            "alert_type": alert_type,
            "details": details or {},
            "ip_address": ip_address,
            "severity": "high",
        }

        self.security_alerts.append(alert)
        logger.warning(f"Security alert: {alert_type} for user {user_id}")

        await self.log_event(
            AuditEventType.SECURITY_ALERT,
            user_id,
            details={"alert_type": alert_type, **details},
            ip_address=ip_address,
        )

    async def get_user_audit_trail(
        self,
        user_id: str,
        days: int = 7,
    ) -> List[Dict[str, Any]]:
        """Obtém histórico de auditoria de um usuário."""
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        return [
            event for event in self.user_activities[user_id]
            if event["timestamp"] > cutoff_date
        ]

    async def get_event_summary(self) -> Dict[str, Any]:
        """Obtém resumo de eventos."""
        total_events = len(self.audit_log)
        total_users = len(self.user_activities)
        total_alerts = len(self.security_alerts)

        return {
            "total_events": total_events,
            "total_users": total_users,
            "total_security_alerts": total_alerts,
            "event_breakdown": dict(self.event_counts),
            "recent_alerts": self.security_alerts[-10:],
        }

    async def get_suspicious_activities(self) -> List[Dict[str, Any]]:
        """Identifica atividades suspeitas."""
        suspicious = []

        # Usuários com múltiplas falhas de autenticação
        for user_id, activities in self.user_activities.items():
            hour_ago = datetime.utcnow() - timedelta(hours=1)

            auth_failures = [
                a for a in activities
                if a["event_type"] == AuditEventType.AUTHENTICATION_FAILED.value
                and a["timestamp"] > hour_ago
            ]

            if len(auth_failures) >= 3:
                suspicious.append({
                    "user_id": user_id,
                    "issue": "Multiple authentication failures",
                    "count": len(auth_failures),
                    "timestamp": datetime.utcnow(),
                })

            # Usuários com muitas requisições em pouco tempo
            hour_requests = [
                a for a in activities
                if a["event_type"] == AuditEventType.API_REQUEST.value
                and a["timestamp"] > hour_ago
            ]

            if len(hour_requests) > 100:
                suspicious.append({
                    "user_id": user_id,
                    "issue": "Unusual request volume",
                    "count": len(hour_requests),
                    "timestamp": datetime.utcnow(),
                })

        return suspicious

    async def get_ip_activity(self, ip_address: str) -> Dict[str, Any]:
        """Obtém atividade de um IP."""
        ip_events = [
            e for e in self.audit_log
            if e["ip_address"] == ip_address
        ]

        hour_ago = datetime.utcnow() - timedelta(hours=1)
        recent_events = [
            e for e in ip_events
            if e["timestamp"] > hour_ago
        ]

        return {
            "ip_address": ip_address,
            "total_events": len(ip_events),
            "recent_events": len(recent_events),
            "unique_users": len(set(e["user_id"] for e in ip_events)),
            "event_types": dict(defaultdict(int, {
                e["event_type"]: sum(1 for x in ip_events if x["event_type"] == e["event_type"])
                for e in ip_events
            })),
        }

    async def export_audit_log(
        self,
        start_date: datetime = None,
        end_date: datetime = None,
        event_type: str = None,
    ) -> List[Dict[str, Any]]:
        """Exporta log de auditoria com filtros."""
        filtered_log = self.audit_log

        if start_date:
            filtered_log = [e for e in filtered_log if e["timestamp"] >= start_date]

        if end_date:
            filtered_log = [e for e in filtered_log if e["timestamp"] <= end_date]

        if event_type:
            filtered_log = [e for e in filtered_log if e["event_type"] == event_type]

        return filtered_log

    async def cleanup_old_logs(self, days: int = 30) -> int:
        """Remove logs antigos."""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        initial_count = len(self.audit_log)

        self.audit_log = [
            e for e in self.audit_log if e["timestamp"] > cutoff_date
        ]

        removed = initial_count - len(self.audit_log)
        logger.info(f"Cleaned up {removed} old audit logs")

        return removed
