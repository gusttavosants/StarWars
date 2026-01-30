.PHONY: help install dev test lint format clean deploy docker-up docker-down

help:
	@echo "Star Wars API - Comandos disponíveis"
	@echo ""
	@echo "Desenvolvimento:"
	@echo "  make install       - Instalar dependências"
	@echo "  make dev          - Executar aplicação em desenvolvimento"
	@echo "  make test         - Executar testes"
	@echo "  make test-cov     - Executar testes com cobertura"
	@echo "  make lint         - Executar linting"
	@echo "  make format       - Formatar código"
	@echo "  make clean        - Limpar arquivos temporários"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-up    - Iniciar containers"
	@echo "  make docker-down  - Parar containers"
	@echo ""
	@echo "Deploy:"
	@echo "  make deploy       - Deploy para GCP"

install:
	pip install -r requirements.txt

dev:
	uvicorn src.presentation.main:app --reload

test:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=src --cov-report=html --cov-report=term-missing

test-unit:
	pytest tests/unit/ -v

test-integration:
	pytest tests/integration/ -m integration -v

lint:
	flake8 src/ tests/ --max-line-length=100
	mypy src/ --ignore-missing-imports

format:
	black src/ tests/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f api

docker-test:
	docker-compose exec api pytest tests/ -v

deploy:
	gcloud functions deploy starwars-api \
		--runtime python39 \
		--trigger-http \
		--allow-unauthenticated \
		--entry-point starwars_api \
		--source . \
		--set-env-vars ENVIRONMENT=production,DEBUG=False

deploy-api-gateway:
	gcloud api-gateway apis create starwars-api
	gcloud api-gateway api-configs create v1 \
		--api=starwars-api \
		--openapi-spec=openapi.yaml \
		--backend-auth-service-account=default

docs:
	@echo "Documentação disponível em:"
	@echo "  - Swagger UI: http://localhost:8000/docs"
	@echo "  - ReDoc: http://localhost:8000/redoc"
	@echo "  - OpenAPI JSON: http://localhost:8000/openapi.json"

requirements:
	pip freeze > requirements.txt
