from typing import List, Optional

from pydantic import BaseModel, Field


class Film(BaseModel):
    """Entidade que representa um filme de Star Wars."""

    title: str = Field(..., description="Título do filme")
    episode_id: Optional[int] = Field(None, description="ID do episódio")
    opening_crawl: Optional[str] = Field(None, description="Texto de abertura")
    director: Optional[str] = Field(None, description="Diretor do filme")
    producer: Optional[str] = Field(None, description="Produtor do filme")
    release_date: Optional[str] = Field(None, description="Data de lançamento")
    characters: List[str] = Field(default_factory=list, description="URLs dos personagens")
    planets: List[str] = Field(default_factory=list, description="URLs dos planetas")
    starships: List[str] = Field(default_factory=list, description="URLs das naves")
    vehicles: List[str] = Field(default_factory=list, description="URLs dos veículos")
    species: List[str] = Field(default_factory=list, description="URLs das espécies")
    url: Optional[str] = Field(None, description="URL do recurso")
    created: Optional[str] = Field(None, description="Data de criação")
    edited: Optional[str] = Field(None, description="Data de edição")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "A New Hope",
                "episode_id": 4,
                "opening_crawl": "It is a period of civil war...",
                "director": "George Lucas",
                "producer": "Gary Kurtz, Rick McCallum",
                "release_date": "1977-05-25",
                "characters": ["https://swapi.dev/api/people/1/"],
                "planets": ["https://swapi.dev/api/planets/1/"],
                "starships": ["https://swapi.dev/api/starships/12/"],
                "vehicles": ["https://swapi.dev/api/vehicles/14/"],
                "species": ["https://swapi.dev/api/species/1/"],
            }
        }

    def get_id(self) -> Optional[str]:
        """Extrai o ID da URL do recurso."""
        if self.url:
            return self.url.rstrip("/").split("/")[-1]
        return None
