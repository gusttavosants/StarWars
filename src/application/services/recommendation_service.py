import logging
from typing import List, Dict, Any, Set
from collections import Counter
import asyncio

logger = logging.getLogger(__name__)


class RecommendationService:
    """Serviço de recomendações inteligentes baseado em correlações."""

    def __init__(self):
        self.user_history: Dict[str, Set[str]] = {}
        self.view_count: Dict[str, int] = {}

    async def track_view(self, user_id: str, resource_id: str, resource_type: str) -> None:
        """Rastreia visualizações de usuários."""
        key = f"{resource_type}:{resource_id}"

        if user_id not in self.user_history:
            self.user_history[user_id] = set()

        self.user_history[user_id].add(key)
        self.view_count[key] = self.view_count.get(key, 0) + 1

        logger.debug(f"Tracked view: {user_id} -> {key}")

    async def get_recommendations_for_character(
        self,
        character_id: str,
        character_service,
        film_service,
        starship_service,
        limit: int = 5,
    ) -> Dict[str, Any]:
        """Obtém recomendações relacionadas a um personagem."""
        try:
            character = await character_service.get_character_by_id(character_id)

            recommendations = {
                "character": character.name,
                "films": [],
                "starships": [],
                "related_characters": [],
            }

            # Filmes do personagem
            if character.films:
                film_ids = [url.split("/")[-2] for url in character.films[:limit]]
                for film_id in film_ids:
                    try:
                        film = await film_service.get_film_by_id(film_id)
                        recommendations["films"].append({
                            "title": film.title,
                            "episode": film.episode_id,
                        })
                    except Exception:
                        pass

            # Naves do personagem
            if character.starships:
                starship_ids = [url.split("/")[-2] for url in character.starships[:limit]]
                for starship_id in starship_ids:
                    try:
                        starship = await starship_service.get_starship_by_id(starship_id)
                        recommendations["starships"].append({
                            "name": starship.name,
                            "class": starship.starship_class,
                        })
                    except Exception:
                        pass

            return recommendations
        except Exception as e:
            logger.error(f"Error getting recommendations: {str(e)}")
            return {}

    async def get_recommendations_for_film(
        self,
        film_id: str,
        film_service,
        character_service,
        planet_service,
        limit: int = 5,
    ) -> Dict[str, Any]:
        """Obtém recomendações relacionadas a um filme."""
        try:
            film = await film_service.get_film_by_id(film_id)

            recommendations = {
                "film": film.title,
                "main_characters": [],
                "planets": [],
                "similar_episodes": [],
            }

            # Personagens principais
            if film.characters:
                char_ids = [url.split("/")[-2] for url in film.characters[:limit]]
                for char_id in char_ids:
                    try:
                        character = await character_service.get_character_by_id(char_id)
                        recommendations["main_characters"].append(character.name)
                    except Exception:
                        pass

            # Planetas
            if film.planets:
                planet_ids = [url.split("/")[-2] for url in film.planets[:limit]]
                for planet_id in planet_ids:
                    try:
                        planet = await planet_service.get_planet_by_id(planet_id)
                        recommendations["planets"].append(planet.name)
                    except Exception:
                        pass

            return recommendations
        except Exception as e:
            logger.error(f"Error getting recommendations: {str(e)}")
            return {}

    async def get_trending_resources(self) -> Dict[str, List[Dict[str, Any]]]:
        """Obtém recursos em alta (mais visualizados)."""
        sorted_views = sorted(
            self.view_count.items(),
            key=lambda x: x[1],
            reverse=True,
        )

        trending = {
            "characters": [],
            "films": [],
            "planets": [],
            "starships": [],
        }

        for resource_key, count in sorted_views[:20]:
            resource_type, resource_id = resource_key.split(":")
            trending[f"{resource_type}s"].append({
                "id": resource_id,
                "views": count,
            })

        return trending

    async def get_user_recommendations(
        self,
        user_id: str,
        all_resources: Dict[str, List[str]],
        limit: int = 5,
    ) -> Dict[str, List[str]]:
        """Obtém recomendações personalizadas para um usuário."""
        if user_id not in self.user_history:
            return {"message": "Sem histórico de visualizações"}

        user_views = self.user_history[user_id]
        resource_types = Counter(v.split(":")[0] for v in user_views)

        recommendations = {}

        for resource_type, count in resource_types.most_common():
            viewed_ids = {v.split(":")[1] for v in user_views if v.startswith(resource_type)}
            available = set(all_resources.get(f"{resource_type}s", []))
            unviewed = available - viewed_ids

            recommendations[f"{resource_type}s"] = list(unviewed)[:limit]

        return recommendations

    async def get_correlation_score(
        self,
        resource_id_1: str,
        resource_id_2: str,
        correlation_data: Dict[str, List[str]],
    ) -> float:
        """Calcula score de correlação entre dois recursos."""
        score = 0.0

        for resource_type, related_ids in correlation_data.items():
            if resource_id_1 in related_ids and resource_id_2 in related_ids:
                score += 1.0

        return min(score, 1.0)
