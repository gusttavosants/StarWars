from typing import Optional, List, Any
from pydantic import BaseModel, Field


class FilterCriteria(BaseModel):
    """Critério de filtro."""

    field: str = Field(..., description="Nome do campo a filtrar")
    operator: str = Field(default="eq", description="Operador de comparação")
    value: Any = Field(..., description="Valor para comparação")


class SortCriteria(BaseModel):
    """Critério de ordenação."""

    field: str = Field(..., description="Campo para ordenar")
    order: str = Field(default="asc", description="Ordem: asc ou desc")


class PaginationParams(BaseModel):
    """Parâmetros de paginação."""

    page: int = Field(default=1, ge=1, description="Número da página")
    page_size: int = Field(default=10, ge=1, le=100, description="Tamanho da página")


class QueryParams(BaseModel):
    """Parâmetros de query."""

    search: Optional[str] = Field(None, description="Termo de busca")
    filters: Optional[List[FilterCriteria]] = Field(None, description="Filtros")
    sort: Optional[SortCriteria] = Field(None, description="Ordenação")
    pagination: PaginationParams = Field(default_factory=PaginationParams)


class PaginatedResponse(BaseModel):
    """Resposta paginada genérica."""

    items: List[Any] = Field(..., description="Itens da página")
    total: int = Field(..., description="Total de itens")
    page: int = Field(..., description="Página atual")
    page_size: int = Field(..., description="Tamanho da página")
    total_pages: int = Field(..., description="Total de páginas")

    class Config:
        json_schema_extra = {
            "example": {
                "items": [],
                "total": 100,
                "page": 1,
                "page_size": 10,
                "total_pages": 10,
            }
        }


class ErrorResponse(BaseModel):
    """Resposta de erro."""

    error: str = Field(..., description="Tipo de erro")
    message: str = Field(..., description="Mensagem de erro")
    status_code: int = Field(..., description="Código HTTP")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "ResourceNotFoundError",
                "message": "Personagem com ID '1' não encontrado",
                "status_code": 404,
            }
        }
