# Guia de Setup - Star Wars API

## Pré-requisitos

- Python 3.9+
- pip ou poetry
- Git
- Redis (opcional, para produção)
- Conta GCP (para deploy)

## Setup Local

### 1. Clonar o Repositório

```bash
git clone <seu-repositorio>
cd starwars-api
```

### 2. Criar Ambiente Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar .env com suas configurações
# Mínimo necessário:
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=DEBUG
```

### 5. Executar a Aplicação

```bash
# Desenvolvimento com reload automático
uvicorn src.presentation.main:app --reload

# Produção
uvicorn src.presentation.main:app --host 0.0.0.0 --port 8000
```

A API estará disponível em `http://localhost:8000`

### 6. Acessar Documentação

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Configuração com Redis (Produção)

### 1. Instalar Redis

**Windows (WSL2):**
```bash
# No WSL2
sudo apt-get install redis-server
redis-server
```

**macOS:**
```bash
brew install redis
redis-server
```

**Docker:**
```bash
docker run -d -p 6379:6379 redis:latest
```

### 2. Configurar Variáveis de Ambiente

```bash
CACHE_ENABLED=True
REDIS_URL=redis://localhost:6379/0
```

### 3. Testar Conexão

```bash
# Python
python -c "import redis; r = redis.Redis.from_url('redis://localhost:6379/0'); print(r.ping())"
```

## Testes

### Executar Todos os Testes

```bash
pytest
```

### Testes com Cobertura

```bash
pytest --cov=src tests/
```

### Apenas Testes Unitários

```bash
pytest tests/unit/
```

### Apenas Testes de Integração

```bash
pytest tests/integration/ -m integration
```

### Testes de um Arquivo Específico

```bash
pytest tests/unit/test_character_service.py -v
```

### Testes com Output Detalhado

```bash
pytest -vv --tb=short
```

## Linting e Formatação

### Black (Formatação)

```bash
# Formatar todos os arquivos
black src/ tests/

# Verificar sem modificar
black --check src/ tests/
```

### Flake8 (Linting)

```bash
# Verificar estilo
flake8 src/ tests/

# Com configuração customizada
flake8 src/ tests/ --max-line-length=100
```

### MyPy (Type Checking)

```bash
# Verificar tipos
mypy src/

# Com configuração
mypy src/ --ignore-missing-imports
```

## Estrutura de Projeto

```
starwars-api/
├── src/
│   ├── config/              # Configurações
│   ├── domain/              # Entidades e interfaces
│   ├── infrastructure/      # Implementações
│   ├── application/         # Lógica de negócio
│   └── presentation/        # API e rotas
├── tests/
│   ├── unit/               # Testes unitários
│   └── integration/        # Testes de integração
├── docs/                   # Documentação
├── requirements.txt        # Dependências
├── pytest.ini             # Configuração pytest
├── .env.example           # Variáveis de exemplo
├── .gitignore            # Arquivos ignorados
├── README.md             # Documentação principal
└── main.py              # Entry point Cloud Functions
```

## Variáveis de Ambiente

### Desenvolvimento

```bash
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=DEBUG
CACHE_ENABLED=False
JWT_SECRET_KEY=dev-secret-key
```

### Produção

```bash
ENVIRONMENT=production
DEBUG=False
LOG_LEVEL=INFO
CACHE_ENABLED=True
REDIS_URL=redis://your-redis-host:6379/0
JWT_SECRET_KEY=your-secure-secret-key
GCP_PROJECT_ID=your-gcp-project
```

## Deploy em GCP

### 1. Preparar Projeto GCP

```bash
# Instalar Google Cloud SDK
# https://cloud.google.com/sdk/docs/install

# Autenticar
gcloud auth login

# Definir projeto
gcloud config set project YOUR_PROJECT_ID
```

### 2. Criar Cloud Function

```bash
gcloud functions deploy starwars-api \
  --runtime python39 \
  --trigger-http \
  --allow-unauthenticated \
  --entry-point starwars_api \
  --source . \
  --set-env-vars ENVIRONMENT=production,DEBUG=False
```

### 3. Configurar API Gateway

```bash
# Criar arquivo openapi.yaml
# Configurar rotas e autenticação
# Deploy do API Gateway

gcloud api-gateway apis create starwars-api
gcloud api-gateway api-configs create v1 \
  --api=starwars-api \
  --openapi-spec=openapi.yaml \
  --backend-auth-service-account=YOUR_SERVICE_ACCOUNT
```

### 4. Configurar Redis Cloud

```bash
# Criar instância Redis no GCP Memorystore
# Obter URL de conexão
# Configurar variável REDIS_URL
```

### 5. Configurar Secret Manager

```bash
# Armazenar JWT_SECRET_KEY
gcloud secrets create jwt-secret-key \
  --replication-policy="automatic" \
  --data-file=-

# Usar em Cloud Function
gcloud functions deploy starwars-api \
  --set-env-vars JWT_SECRET_KEY=projects/YOUR_PROJECT/secrets/jwt-secret-key/versions/latest
```

## Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'src'"

**Solução:**
```bash
# Adicionar diretório ao PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Ou executar do diretório raiz
python -m pytest tests/
```

### Erro: "Connection refused" ao conectar Redis

**Solução:**
```bash
# Verificar se Redis está rodando
redis-cli ping

# Se não estiver, iniciar
redis-server

# Ou usar Docker
docker run -d -p 6379:6379 redis:latest
```

### Erro: "SWAPI API indisponível"

**Solução:**
```bash
# Verificar conectividade
curl https://swapi.dev/api/people/1/

# Aumentar timeout
SWAPI_TIMEOUT=30
```

### Erro: "Invalid JWT token"

**Solução:**
```bash
# Gerar novo token
python -c "
from src.application.security.jwt_handler import JWTHandler
token = JWTHandler.create_token({'sub': 'test-user'})
print(f'Token: {token}')
"

# Usar token em requisições
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/characters
```

## Desenvolvimento

### Adicionar Nova Rota

1. Criar serviço em `src/application/services/`
2. Criar repositório em `src/infrastructure/database/repositories/`
3. Criar rotas em `src/presentation/api/routes/`
4. Incluir router em `src/presentation/main.py`
5. Adicionar testes em `tests/unit/` e `tests/integration/`

### Adicionar Novo Serviço

```python
# src/application/services/new_service.py
from src.infrastructure.database.repositories.new_repository import NewRepository

class NewService:
    def __init__(self, repository: NewRepository):
        self.repository = repository

    async def get_item(self, item_id: str):
        return await self.repository.get_by_id(item_id)
```

### Adicionar Testes

```python
# tests/unit/test_new_service.py
import pytest
from src.application.services.new_service import NewService

@pytest.fixture
def new_service(mock_repository):
    return NewService(mock_repository)

@pytest.mark.asyncio
async def test_get_item(new_service, mock_repository):
    # Arrange
    mock_repository.get_by_id.return_value = {"id": "1", "name": "Item"}

    # Act
    result = await new_service.get_item("1")

    # Assert
    assert result["name"] == "Item"
```

## Contribuindo

1. Criar branch para feature: `git checkout -b feature/nova-funcionalidade`
2. Fazer commits descritivos: `git commit -m "feat: adiciona nova funcionalidade"`
3. Push para branch: `git push origin feature/nova-funcionalidade`
4. Abrir Pull Request

## Padrão de Commits

```
feat: adiciona nova funcionalidade
fix: corrige bug
docs: atualiza documentação
test: adiciona testes
refactor: refatora código
style: muda estilo (sem lógica)
chore: atualiza dependências
```

## Recursos Úteis

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [SWAPI Documentation](https://swapi.dev/)
- [GCP Cloud Functions](https://cloud.google.com/functions/docs)
- [Redis Documentation](https://redis.io/documentation)
- [JWT.io](https://jwt.io/)

## Suporte

Para dúvidas ou problemas:
1. Verificar documentação
2. Buscar em issues existentes
3. Abrir nova issue com detalhes
4. Contactar time de desenvolvimento
