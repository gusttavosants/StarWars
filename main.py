import functions_framework

from src.presentation.main import app


@functions_framework.http
def starwars_api(request):
    """Handler para Google Cloud Functions."""
    return app(request)
