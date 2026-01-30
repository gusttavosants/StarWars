from typing import List, Optional

from pydantic import BaseModel, Field


class Starship(BaseModel):
    """Entidade que representa uma nave estelar de Star Wars."""

    name: str = Field(..., description="Nome da nave")
    model: Optional[str] = Field(None, description="Modelo da nave")
    manufacturer: Optional[str] = Field(None, description="Fabricante")
    cost_in_credits: Optional[str] = Field(None, description="Custo em créditos")
    length: Optional[str] = Field(None, description="Comprimento em metros")
    max_atmosphering_speed: Optional[str] = Field(
        None, description="Velocidade máxima na atmosfera"
    )
    crew: Optional[str] = Field(None, description="Número de tripulantes")
    passengers: Optional[str] = Field(None, description="Número de passageiros")
    cargo_capacity: Optional[str] = Field(None, description="Capacidade de carga")
    consumables: Optional[str] = Field(None, description="Consumíveis")
    hyperdrive_rating: Optional[str] = Field(None, description="Classificação do hipermotor")
    mglt: Optional[str] = Field(None, alias="MGLT", description="Megatons por luz")
    starship_class: Optional[str] = Field(None, description="Classe da nave")
    pilots: List[str] = Field(default_factory=list, description="URLs dos pilotos")
    films: List[str] = Field(default_factory=list, description="URLs dos filmes")
    url: Optional[str] = Field(None, description="URL do recurso")
    created: Optional[str] = Field(None, description="Data de criação")
    edited: Optional[str] = Field(None, description="Data de edição")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "X-wing",
                "model": "T-65 X-wing starfighter",
                "manufacturer": "Incom Corporation",
                "cost_in_credits": "149999",
                "length": "12.9",
                "max_atmosphering_speed": "1050",
                "crew": "1",
                "passengers": "0",
                "cargo_capacity": "110",
                "consumables": "5 days",
                "hyperdrive_rating": "1.0",
                "MGLT": "100",
                "starship_class": "Starfighter",
                "pilots": ["https://swapi.dev/api/people/1/"],
                "films": ["https://swapi.dev/api/films/1/"],
            }
        }

    def get_id(self) -> Optional[str]:
        """Extrai o ID da URL do recurso."""
        if self.url:
            return self.url.rstrip("/").split("/")[-1]
        return None
