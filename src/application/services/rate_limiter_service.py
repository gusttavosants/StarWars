import logging
from typing import Dict, Tuple
from datetime import datetime, timedelta
from collections import defaultdict
import asyncio

logger = logging.getLogger(__name__)


class RateLimiterService:
    """Serviço de rate limiting inteligente por usuário e endpoint."""

    def __init__(
        self,
        default_requests_per_hour: int = 100,
        default_requests_per_minute: int = 10,
    ):
        self.default_requests_per_hour = default_requests_per_hour
        self.default_requests_per_minute = default_requests_per_minute

        # Rastreamento por usuário
        self.user_requests: Dict[str, list] = defaultdict(list)

        # Rastreamento por endpoint
        self.endpoint_requests: Dict[str, list] = defaultdict(list)

        # Rastreamento por IP
        self.ip_requests: Dict[str, list] = defaultdict(list)

        # Limites customizados por usuário
        self.user_limits: Dict[str, Dict[str, int]] = {}

        # Usuários bloqueados
        self.blocked_users: Dict[str, datetime] = {}

    async def check_rate_limit(
        self,
        user_id: str,
        endpoint: str,
        ip_address: str,
    ) -> Tuple[bool, Dict[str, any]]:
        """Verifica se o usuário pode fazer a requisição."""
        now = datetime.utcnow()

        # Verificar se usuário está bloqueado
        if user_id in self.blocked_users:
            if now < self.blocked_users[user_id]:
                return False, {
                    "error": "User temporarily blocked",
                    "blocked_until": self.blocked_users[user_id],
                }
            else:
                del self.blocked_users[user_id]

        # Limpar requisições antigas
        self._cleanup_old_requests(user_id, endpoint, ip_address)

        # Verificar limite por minuto
        minute_ago = now - timedelta(minutes=1)
        user_minute_requests = [
            r for r in self.user_requests[user_id] if r > minute_ago
        ]

        limit_per_minute = self.user_limits.get(user_id, {}).get(
            "per_minute",
            self.default_requests_per_minute,
        )

        if len(user_minute_requests) >= limit_per_minute:
            return False, {
                "error": "Rate limit exceeded (per minute)",
                "limit": limit_per_minute,
                "current": len(user_minute_requests),
                "reset_in_seconds": int(
                    (user_minute_requests[0] + timedelta(minutes=1) - now).total_seconds()
                ),
            }

        # Verificar limite por hora
        hour_ago = now - timedelta(hours=1)
        user_hour_requests = [
            r for r in self.user_requests[user_id] if r > hour_ago
        ]

        limit_per_hour = self.user_limits.get(user_id, {}).get(
            "per_hour",
            self.default_requests_per_hour,
        )

        if len(user_hour_requests) >= limit_per_hour:
            return False, {
                "error": "Rate limit exceeded (per hour)",
                "limit": limit_per_hour,
                "current": len(user_hour_requests),
                "reset_in_seconds": int(
                    (user_hour_requests[0] + timedelta(hours=1) - now).total_seconds()
                ),
            }

        # Registrar requisição
        self.user_requests[user_id].append(now)
        self.endpoint_requests[endpoint].append(now)
        self.ip_requests[ip_address].append(now)

        return True, {
            "remaining_per_minute": limit_per_minute - len(user_minute_requests) - 1,
            "remaining_per_hour": limit_per_hour - len(user_hour_requests) - 1,
        }

    def _cleanup_old_requests(self, user_id: str, endpoint: str, ip_address: str) -> None:
        """Remove requisições antigas do rastreamento."""
        cutoff_time = datetime.utcnow() - timedelta(hours=2)

        self.user_requests[user_id] = [
            r for r in self.user_requests[user_id] if r > cutoff_time
        ]
        self.endpoint_requests[endpoint] = [
            r for r in self.endpoint_requests[endpoint] if r > cutoff_time
        ]
        self.ip_requests[ip_address] = [
            r for r in self.ip_requests[ip_address] if r > cutoff_time
        ]

    async def set_user_limit(
        self,
        user_id: str,
        requests_per_hour: int,
        requests_per_minute: int,
    ) -> None:
        """Define limite customizado para um usuário."""
        self.user_limits[user_id] = {
            "per_hour": requests_per_hour,
            "per_minute": requests_per_minute,
        }
        logger.info(f"Set custom limit for user {user_id}")

    async def block_user(self, user_id: str, duration_minutes: int = 60) -> None:
        """Bloqueia um usuário temporariamente."""
        self.blocked_users[user_id] = datetime.utcnow() + timedelta(minutes=duration_minutes)
        logger.warning(f"Blocked user {user_id} for {duration_minutes} minutes")

    async def unblock_user(self, user_id: str) -> None:
        """Desbloqueia um usuário."""
        if user_id in self.blocked_users:
            del self.blocked_users[user_id]
            logger.info(f"Unblocked user {user_id}")

    async def get_user_status(self, user_id: str) -> Dict[str, any]:
        """Obtém status de rate limit do usuário."""
        now = datetime.utcnow()

        minute_ago = now - timedelta(minutes=1)
        hour_ago = now - timedelta(hours=1)

        user_minute_requests = len([
            r for r in self.user_requests[user_id] if r > minute_ago
        ])
        user_hour_requests = len([
            r for r in self.user_requests[user_id] if r > hour_ago
        ])

        limit_per_minute = self.user_limits.get(user_id, {}).get(
            "per_minute",
            self.default_requests_per_minute,
        )
        limit_per_hour = self.user_limits.get(user_id, {}).get(
            "per_hour",
            self.default_requests_per_hour,
        )

        is_blocked = user_id in self.blocked_users

        return {
            "user_id": user_id,
            "is_blocked": is_blocked,
            "blocked_until": self.blocked_users.get(user_id),
            "requests_this_minute": user_minute_requests,
            "limit_per_minute": limit_per_minute,
            "requests_this_hour": user_hour_requests,
            "limit_per_hour": limit_per_hour,
            "remaining_per_minute": max(0, limit_per_minute - user_minute_requests),
            "remaining_per_hour": max(0, limit_per_hour - user_hour_requests),
        }

    async def get_endpoint_stats(self, endpoint: str) -> Dict[str, any]:
        """Obtém estatísticas de um endpoint."""
        now = datetime.utcnow()
        hour_ago = now - timedelta(hours=1)

        requests_this_hour = len([
            r for r in self.endpoint_requests[endpoint] if r > hour_ago
        ])

        return {
            "endpoint": endpoint,
            "requests_this_hour": requests_this_hour,
            "total_tracked_requests": len(self.endpoint_requests[endpoint]),
        }

    async def reset_user_limit(self, user_id: str) -> None:
        """Reseta o limite de um usuário para o padrão."""
        if user_id in self.user_limits:
            del self.user_limits[user_id]
            logger.info(f"Reset limit for user {user_id}")
