from typing import List, Optional

from pydantic import BaseModel, Field


class Character(BaseModel):
    """Entidade que representa um personagem de Star Wars."""

    name: str = Field(..., description="Nome do personagem")
    height: Optional[str] = Field(None, description="Altura em centímetros")
    mass: Optional[str] = Field(None, description="Massa em quilogramas")
    hair_color: Optional[str] = Field(None, description="Cor do cabelo")
    skin_color: Optional[str] = Field(None, description="Cor da pele")
    eye_color: Optional[str] = Field(None, description="Cor dos olhos")
    birth_year: Optional[str] = Field(None, description="Ano de nascimento")
    gender: Optional[str] = Field(None, description="Gênero")
    homeworld: Optional[str] = Field(None, description="URL do planeta natal")
    films: List[str] = Field(default_factory=list, description="URLs dos filmes")
    species: List[str] = Field(default_factory=list, description="URLs das espécies")
    vehicles: List[str] = Field(default_factory=list, description="URLs dos veículos")
    starships: List[str] = Field(default_factory=list, description="URLs das naves estelares")
    url: Optional[str] = Field(None, description="URL do recurso")
    created: Optional[str] = Field(None, description="Data de criação")
    edited: Optional[str] = Field(None, description="Data de edição")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Luke Skywalker",
                "height": "172",
                "mass": "77",
                "hair_color": "blond",
                "skin_color": "fair",
                "eye_color": "blue",
                "birth_year": "19BBY",
                "gender": "male",
                "homeworld": "https://swapi.dev/api/planets/1/",
                "films": ["https://swapi.dev/api/films/1/"],
                "species": ["https://swapi.dev/api/species/1/"],
                "vehicles": ["https://swapi.dev/api/vehicles/14/"],
                "starships": ["https://swapi.dev/api/starships/12/"],
            }
        }

    def get_id(self) -> Optional[str]:
        """Extrai o ID da URL do recurso."""
        if self.url:
            return self.url.rstrip("/").split("/")[-1]
        return None
