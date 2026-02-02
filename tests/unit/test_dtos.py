import pytest
from pydantic import ValidationError

from src.application.dto.filters import (
    ErrorResponse,
    FilterCriteria,
    PaginatedResponse,
    PaginationParams,
    QueryParams,
    SortCriteria,
)


class TestFilterCriteria:
    """Testes para FilterCriteria DTO."""

    def test_filter_criteria_creation(self):
        """Testa criação de critério de filtro."""
        filter_obj = FilterCriteria(field="gender", operator="eq", value="male")

        assert filter_obj.field == "gender"
        assert filter_obj.operator == "eq"
        assert filter_obj.value == "male"

    def test_filter_criteria_default_operator(self):
        """Testa operador padrão."""
        filter_obj = FilterCriteria(field="gender", value="male")

        assert filter_obj.operator == "eq"

    def test_filter_criteria_with_list_value(self):
        """Testa critério com valor de lista."""
        filter_obj = FilterCriteria(field="gender", operator="in", value=["male", "female"])

        assert isinstance(filter_obj.value, list)
        assert len(filter_obj.value) == 2

    def test_filter_criteria_missing_field(self):
        """Testa erro quando campo está faltando."""
        with pytest.raises(ValidationError):
            FilterCriteria(operator="eq", value="male")

    def test_filter_criteria_missing_value(self):
        """Testa erro quando valor está faltando."""
        with pytest.raises(ValidationError):
            FilterCriteria(field="gender", operator="eq")


class TestSortCriteria:
    """Testes para SortCriteria DTO."""

    def test_sort_criteria_creation(self):
        """Testa criação de critério de ordenação."""
        sort_obj = SortCriteria(field="name", order="asc")

        assert sort_obj.field == "name"
        assert sort_obj.order == "asc"

    def test_sort_criteria_default_order(self):
        """Testa ordem padrão."""
        sort_obj = SortCriteria(field="name")

        assert sort_obj.order == "asc"

    def test_sort_criteria_desc_order(self):
        """Testa ordem descendente."""
        sort_obj = SortCriteria(field="height", order="desc")

        assert sort_obj.order == "desc"

    def test_sort_criteria_missing_field(self):
        """Testa erro quando campo está faltando."""
        with pytest.raises(ValidationError):
            SortCriteria(order="asc")


class TestPaginationParams:
    """Testes para PaginationParams DTO."""

    def test_pagination_params_creation(self):
        """Testa criação de parâmetros de paginação."""
        params = PaginationParams(page=1, page_size=10)

        assert params.page == 1
        assert params.page_size == 10

    def test_pagination_params_defaults(self):
        """Testa valores padrão."""
        params = PaginationParams()

        assert params.page == 1
        assert params.page_size == 10

    def test_pagination_params_custom_values(self):
        """Testa valores customizados."""
        params = PaginationParams(page=5, page_size=50)

        assert params.page == 5
        assert params.page_size == 50

    def test_pagination_params_invalid_page(self):
        """Testa validação de página."""
        with pytest.raises(ValidationError):
            PaginationParams(page=0)

    def test_pagination_params_invalid_page_size(self):
        """Testa validação de tamanho de página."""
        with pytest.raises(ValidationError):
            PaginationParams(page_size=0)

    def test_pagination_params_max_page_size(self):
        """Testa limite máximo de tamanho de página."""
        with pytest.raises(ValidationError):
            PaginationParams(page_size=101)


class TestQueryParams:
    """Testes para QueryParams DTO."""

    def test_query_params_creation(self):
        """Testa criação de parâmetros de query."""
        params = QueryParams(
            search="luke",
            filters=[FilterCriteria(field="gender", value="male")],
            sort=SortCriteria(field="name"),
        )

        assert params.search == "luke"
        assert len(params.filters) == 1
        assert params.sort.field == "name"

    def test_query_params_minimal(self):
        """Testa criação mínima."""
        params = QueryParams()

        assert params.search is None
        assert params.filters is None
        assert params.sort is None
        assert params.pagination.page == 1

    def test_query_params_with_pagination(self):
        """Testa com parâmetros de paginação."""
        params = QueryParams(pagination=PaginationParams(page=2, page_size=20))

        assert params.pagination.page == 2
        assert params.pagination.page_size == 20

    def test_query_params_multiple_filters(self):
        """Testa com múltiplos filtros."""
        filters = [
            FilterCriteria(field="gender", value="male"),
            FilterCriteria(field="height", operator="gt", value="170"),
        ]
        params = QueryParams(filters=filters)

        assert len(params.filters) == 2


class TestPaginatedResponse:
    """Testes para PaginatedResponse DTO."""

    def test_paginated_response_creation(self):
        """Testa criação de resposta paginada."""
        response = PaginatedResponse(
            items=[{"name": "Luke"}], total=82, page=1, page_size=10, total_pages=9
        )

        assert len(response.items) == 1
        assert response.total == 82
        assert response.page == 1
        assert response.page_size == 10
        assert response.total_pages == 9

    def test_paginated_response_empty_items(self):
        """Testa resposta com itens vazios."""
        response = PaginatedResponse(items=[], total=0, page=1, page_size=10, total_pages=0)

        assert len(response.items) == 0
        assert response.total == 0

    def test_paginated_response_multiple_items(self):
        """Testa resposta com múltiplos itens."""
        items = [{"name": "Luke"}, {"name": "Yoda"}, {"name": "Obi-Wan"}]
        response = PaginatedResponse(items=items, total=82, page=1, page_size=10, total_pages=9)

        assert len(response.items) == 3

    def test_paginated_response_json_serialization(self):
        """Testa serialização JSON."""
        response = PaginatedResponse(
            items=[{"name": "Luke"}], total=82, page=1, page_size=10, total_pages=9
        )

        json_str = response.model_dump_json()
        assert isinstance(json_str, str)
        assert "Luke" in json_str
        assert "82" in json_str


class TestErrorResponse:
    """Testes para ErrorResponse DTO."""

    def test_error_response_creation(self):
        """Testa criação de resposta de erro."""
        error = ErrorResponse(
            error="ResourceNotFoundError", message="Personagem não encontrado", status_code=404
        )

        assert error.error == "ResourceNotFoundError"
        assert error.message == "Personagem não encontrado"
        assert error.status_code == 404

    def test_error_response_different_status_codes(self):
        """Testa diferentes códigos de status."""
        errors = [
            ErrorResponse(error="BadRequest", message="Requisição inválida", status_code=400),
            ErrorResponse(error="Unauthorized", message="Não autorizado", status_code=401),
            ErrorResponse(error="NotFound", message="Não encontrado", status_code=404),
            ErrorResponse(error="ServerError", message="Erro interno", status_code=500),
        ]

        assert errors[0].status_code == 400
        assert errors[1].status_code == 401
        assert errors[2].status_code == 404
        assert errors[3].status_code == 500

    def test_error_response_json_serialization(self):
        """Testa serialização JSON."""
        error = ErrorResponse(
            error="ResourceNotFoundError", message="Personagem não encontrado", status_code=404
        )

        json_str = error.model_dump_json()
        assert isinstance(json_str, str)
        assert "ResourceNotFoundError" in json_str
        assert "404" in json_str

    def test_error_response_dict_conversion(self):
        """Testa conversão para dict."""
        error = ErrorResponse(
            error="ResourceNotFoundError", message="Personagem não encontrado", status_code=404
        )

        data = error.model_dump()
        assert isinstance(data, dict)
        assert data["error"] == "ResourceNotFoundError"
        assert data["status_code"] == 404


class TestDTOValidation:
    """Testes para validação de DTOs."""

    def test_filter_criteria_with_numeric_value(self):
        """Testa filtro com valor numérico."""
        filter_obj = FilterCriteria(field="height", operator="gt", value=170)

        assert filter_obj.value == 170

    def test_filter_criteria_with_dict_value(self):
        """Testa filtro com valor de dicionário."""
        filter_obj = FilterCriteria(field="metadata", operator="eq", value={"key": "value"})

        assert isinstance(filter_obj.value, dict)

    def test_pagination_params_boundary_values(self):
        """Testa valores limítrofes de paginação."""
        # Página mínima
        params1 = PaginationParams(page=1, page_size=1)
        assert params1.page == 1
        assert params1.page_size == 1

        # Página máxima
        params2 = PaginationParams(page=1000, page_size=100)
        assert params2.page == 1000
        assert params2.page_size == 100

    def test_query_params_with_all_fields(self):
        """Testa QueryParams com todos os campos."""
        params = QueryParams(
            search="luke",
            filters=[FilterCriteria(field="gender", value="male")],
            sort=SortCriteria(field="name", order="asc"),
            pagination=PaginationParams(page=1, page_size=10),
        )

        assert params.search == "luke"
        assert params.filters is not None
        assert params.sort is not None
        assert params.pagination is not None
