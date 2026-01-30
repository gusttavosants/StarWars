import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta
from collections import defaultdict
import asyncio

logger = logging.getLogger(__name__)


class AnalyticsService:
    """Serviço para análise e estatísticas da API."""

    def __init__(self):
        self.request_log: List[Dict[str, Any]] = []
        self.endpoint_stats: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
            "total_requests": 0,
            "avg_response_time": 0,
            "error_count": 0,
            "last_accessed": None,
        })
        self.user_stats: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
            "total_requests": 0,
            "endpoints_accessed": set(),
            "last_request": None,
        })

    async def log_request(
        self,
        endpoint: str,
        user_id: str,
        response_time: float,
        status_code: int,
        method: str = "GET",
    ) -> None:
        """Registra uma requisição para análise."""
        request_data = {
            "timestamp": datetime.utcnow(),
            "endpoint": endpoint,
            "user_id": user_id,
            "response_time": response_time,
            "status_code": status_code,
            "method": method,
        }

        self.request_log.append(request_data)

        # Atualizar estatísticas de endpoint
        self.endpoint_stats[endpoint]["total_requests"] += 1
        self.endpoint_stats[endpoint]["last_accessed"] = datetime.utcnow()

        if status_code >= 400:
            self.endpoint_stats[endpoint]["error_count"] += 1

        # Atualizar estatísticas de usuário
        self.user_stats[user_id]["total_requests"] += 1
        self.user_stats[user_id]["endpoints_accessed"].add(endpoint)
        self.user_stats[user_id]["last_request"] = datetime.utcnow()

        logger.debug(f"Request logged: {endpoint} by {user_id} ({response_time}ms)")

    async def get_endpoint_stats(self, endpoint: str = None) -> Dict[str, Any]:
        """Obtém estatísticas de endpoints."""
        if endpoint:
            return self.endpoint_stats.get(endpoint, {})

        return dict(self.endpoint_stats)

    async def get_user_stats(self, user_id: str = None) -> Dict[str, Any]:
        """Obtém estatísticas de usuários."""
        if user_id:
            stats = self.user_stats.get(user_id, {})
            return {
                **stats,
                "endpoints_accessed": list(stats.get("endpoints_accessed", [])),
            }

        return {
            user: {
                **stats,
                "endpoints_accessed": list(stats.get("endpoints_accessed", [])),
            }
            for user, stats in self.user_stats.items()
        }

    async def get_top_endpoints(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Obtém endpoints mais acessados."""
        sorted_endpoints = sorted(
            self.endpoint_stats.items(),
            key=lambda x: x[1]["total_requests"],
            reverse=True,
        )

        return [
            {
                "endpoint": endpoint,
                "requests": stats["total_requests"],
                "errors": stats["error_count"],
                "last_accessed": stats["last_accessed"],
            }
            for endpoint, stats in sorted_endpoints[:limit]
        ]

    async def get_top_users(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Obtém usuários mais ativos."""
        sorted_users = sorted(
            self.user_stats.items(),
            key=lambda x: x[1]["total_requests"],
            reverse=True,
        )

        return [
            {
                "user_id": user_id,
                "requests": stats["total_requests"],
                "endpoints_count": len(stats.get("endpoints_accessed", [])),
                "last_request": stats["last_request"],
            }
            for user_id, stats in sorted_users[:limit]
        ]

    async def get_performance_metrics(self) -> Dict[str, Any]:
        """Obtém métricas de performance."""
        if not self.request_log:
            return {
                "total_requests": 0,
                "avg_response_time": 0,
                "error_rate": 0,
                "uptime": "100%",
            }

        total_requests = len(self.request_log)
        avg_response_time = sum(r["response_time"] for r in self.request_log) / total_requests
        error_count = sum(1 for r in self.request_log if r["status_code"] >= 400)
        error_rate = (error_count / total_requests) * 100 if total_requests > 0 else 0

        return {
            "total_requests": total_requests,
            "avg_response_time": round(avg_response_time, 2),
            "error_rate": round(error_rate, 2),
            "unique_users": len(self.user_stats),
            "unique_endpoints": len(self.endpoint_stats),
        }

    async def get_hourly_stats(self) -> Dict[str, int]:
        """Obtém estatísticas por hora."""
        hourly_stats = defaultdict(int)

        for request in self.request_log:
            hour = request["timestamp"].strftime("%Y-%m-%d %H:00")
            hourly_stats[hour] += 1

        return dict(sorted(hourly_stats.items()))

    async def clear_old_logs(self, days: int = 7) -> int:
        """Remove logs antigos."""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        initial_count = len(self.request_log)

        self.request_log = [
            r for r in self.request_log if r["timestamp"] > cutoff_date
        ]

        removed = initial_count - len(self.request_log)
        logger.info(f"Removed {removed} old logs")

        return removed
