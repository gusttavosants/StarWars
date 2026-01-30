from typing import List, Optional

from pydantic import BaseModel, Field


class Planet(BaseModel):
    """Entidade que representa um planeta de Star Wars."""

    name: str = Field(..., description="Nome do planeta")
    rotation_period: Optional[str] = Field(None, description="Período de rotação")
    orbital_period: Optional[str] = Field(None, description="Período orbital")
    diameter: Optional[str] = Field(None, description="Diâmetro em quilômetros")
    climate: Optional[str] = Field(None, description="Clima do planeta")
    gravity: Optional[str] = Field(None, description="Gravidade")
    terrain: Optional[str] = Field(None, description="Terreno")
    surface_water: Optional[str] = Field(None, description="Percentual de água")
    population: Optional[str] = Field(None, description="População")
    residents: List[str] = Field(default_factory=list, description="URLs dos residentes")
    films: List[str] = Field(default_factory=list, description="URLs dos filmes")
    url: Optional[str] = Field(None, description="URL do recurso")
    created: Optional[str] = Field(None, description="Data de criação")
    edited: Optional[str] = Field(None, description="Data de edição")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Tatooine",
                "rotation_period": "23",
                "orbital_period": "304",
                "diameter": "10465",
                "climate": "arid",
                "gravity": "1 standard",
                "terrain": "desert",
                "surface_water": "1",
                "population": "200000",
                "residents": ["https://swapi.dev/api/people/1/"],
                "films": ["https://swapi.dev/api/films/1/"],
            }
        }

    def get_id(self) -> Optional[str]:
        """Extrai o ID da URL do recurso."""
        if self.url:
            return self.url.rstrip("/").split("/")[-1]
        return None
