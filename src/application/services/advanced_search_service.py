import logging
from typing import List, Dict, Any, Tuple
from difflib import SequenceMatcher
import re

logger = logging.getLogger(__name__)


class AdvancedSearchService:
    """Serviço de busca avançada com scoring de relevância."""

    @staticmethod
    def calculate_relevance_score(query: str, target: str) -> float:
        """Calcula score de relevância entre query e target."""
        query_lower = query.lower()
        target_lower = target.lower()

        score = 0.0

        # Correspondência exata (100%)
        if query_lower == target_lower:
            return 1.0

        # Começa com (80%)
        if target_lower.startswith(query_lower):
            score += 0.8

        # Contém (60%)
        if query_lower in target_lower:
            score += 0.6

        # Similaridade de sequência (até 50%)
        similarity = SequenceMatcher(None, query_lower, target_lower).ratio()
        score += similarity * 0.5

        # Penalidade por tamanho (quanto maior a diferença, menor o score)
        size_diff = abs(len(query) - len(target)) / max(len(query), len(target))
        score -= size_diff * 0.1

        return max(0.0, min(score, 1.0))

    @staticmethod
    def tokenize_query(query: str) -> List[str]:
        """Tokeniza uma query em palavras-chave."""
        # Remove caracteres especiais e divide por espaço
        tokens = re.findall(r'\b\w+\b', query.lower())
        return tokens

    async def search_with_scoring(
        self,
        query: str,
        resources: List[Dict[str, Any]],
        search_fields: List[str],
        min_score: float = 0.3,
    ) -> List[Tuple[Dict[str, Any], float]]:
        """Busca recursos com scoring de relevância."""
        tokens = self.tokenize_query(query)

        results = []

        for resource in resources:
            total_score = 0.0
            matched_fields = 0

            for field in search_fields:
                if field not in resource:
                    continue

                field_value = str(resource[field]).lower()

                # Calcular score para cada token
                field_score = 0.0
                for token in tokens:
                    token_score = self.calculate_relevance_score(token, field_value)
                    field_score = max(field_score, token_score)

                if field_score > 0:
                    total_score += field_score
                    matched_fields += 1

            # Média de scores dos campos que tiveram match
            if matched_fields > 0:
                avg_score = total_score / matched_fields

                if avg_score >= min_score:
                    results.append((resource, avg_score))

        # Ordenar por score descendente
        results.sort(key=lambda x: x[1], reverse=True)

        return results

    async def fuzzy_search(
        self,
        query: str,
        resources: List[Dict[str, Any]],
        search_field: str,
        threshold: float = 0.6,
    ) -> List[Dict[str, Any]]:
        """Busca fuzzy (tolerante a erros de digitação)."""
        results = []

        for resource in resources:
            if search_field not in resource:
                continue

            field_value = str(resource[search_field])
            score = self.calculate_relevance_score(query, field_value)

            if score >= threshold:
                results.append(resource)

        return results

    async def search_with_filters(
        self,
        query: str,
        resources: List[Dict[str, Any]],
        search_fields: List[str],
        filters: Dict[str, Any] = None,
        min_score: float = 0.3,
    ) -> List[Tuple[Dict[str, Any], float]]:
        """Busca com filtros adicionais."""
        # Aplicar filtros primeiro
        filtered_resources = resources

        if filters:
            for field, value in filters.items():
                filtered_resources = [
                    r for r in filtered_resources
                    if field in r and str(r[field]).lower() == str(value).lower()
                ]

        # Depois fazer busca com scoring
        return await self.search_with_scoring(
            query,
            filtered_resources,
            search_fields,
            min_score,
        )

    async def autocomplete(
        self,
        query: str,
        resources: List[Dict[str, Any]],
        field: str,
        limit: int = 10,
    ) -> List[str]:
        """Sugestões de autocompletar."""
        query_lower = query.lower()
        suggestions = set()

        for resource in resources:
            if field not in resource:
                continue

            value = str(resource[field]).lower()

            # Sugestões que começam com a query
            if value.startswith(query_lower):
                suggestions.add(resource[field])

        return sorted(list(suggestions))[:limit]

    async def get_search_suggestions(
        self,
        query: str,
        resources: List[Dict[str, Any]],
        fields: List[str],
        limit: int = 5,
    ) -> Dict[str, List[str]]:
        """Obtém sugestões de busca por campo."""
        query_lower = query.lower()
        suggestions = {}

        for field in fields:
            field_suggestions = set()

            for resource in resources:
                if field not in resource:
                    continue

                value = str(resource[field]).lower()

                if query_lower in value:
                    field_suggestions.add(resource[field])

            if field_suggestions:
                suggestions[field] = sorted(list(field_suggestions))[:limit]

        return suggestions

    async def search_by_similarity(
        self,
        query: str,
        resources: List[Dict[str, Any]],
        field: str,
        threshold: float = 0.7,
    ) -> List[Tuple[Dict[str, Any], float]]:
        """Busca por similaridade usando SequenceMatcher."""
        results = []

        for resource in resources:
            if field not in resource:
                continue

            value = str(resource[field])
            similarity = SequenceMatcher(None, query.lower(), value.lower()).ratio()

            if similarity >= threshold:
                results.append((resource, similarity))

        results.sort(key=lambda x: x[1], reverse=True)

        return results
