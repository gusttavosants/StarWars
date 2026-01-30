# Arquitetura Técnica - Star Wars API

## 1. Visão Geral

A Star Wars API é uma plataforma moderna construída com **Clean Architecture** e princípios **SOLID**, permitindo explorar dados de Star Wars através de uma API RESTful robusta e escalável.

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                        │
│  (FastAPI Routes, Error Handlers, Middleware)               │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                  Application Layer                           │
│  (Services, DTOs, Security, Business Logic)                 │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                   Domain Layer                               │
│  (Entities, Interfaces, Business Rules)                     │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              Infrastructure Layer                            │
│  (HTTP Client, Cache, Repositories, Database)               │
└─────────────────────────────────────────────────────────────┘
```

## 2. Camadas da Arquitetura

### 2.1 Presentation Layer (Camada de Apresentação)

Responsável pela exposição da API e tratamento de requisições HTTP.

**Componentes:**
- **Routes**: Endpoints da API organizados por recurso
  - `characters.py`: Endpoints para personagens
  - `planets.py`: Endpoints para planetas
  - `starships.py`: Endpoints para naves
  - `films.py`: Endpoints para filmes

- **Middleware**: Processamento de requisições/respostas
  - `error_handler.py`: Tratamento centralizado de erros
  - `auth_middleware.py`: Validação de autenticação

- **Main**: Configuração da aplicação FastAPI

**Responsabilidades:**
- Receber requisições HTTP
- Validar parâmetros de entrada
- Chamar serviços apropriados
- Retornar respostas formatadas
- Tratar exceções

### 2.2 Application Layer (Camada de Aplicação)

Contém a lógica de negócio e orquestração entre camadas.

**Componentes:**
- **Services**: Lógica de negócio
  - `character_service.py`: Operações com personagens
  - `planet_service.py`: Operações com planetas
  - `starship_service.py`: Operações com naves
  - `film_service.py`: Operações com filmes

- **DTOs**: Objetos de transferência de dados
  - `filters.py`: Modelos para filtros, paginação, respostas

- **Security**: Autenticação e autorização
  - `jwt_handler.py`: Geração e validação de JWT
  - `auth.py`: Dependências de autenticação

**Responsabilidades:**
- Orquestrar operações entre repositórios
- Implementar regras de negócio
- Validar dados
- Gerenciar transações
- Implementar correlações entre recursos

### 2.3 Domain Layer (Camada de Domínio)

Define as regras de negócio e contratos da aplicação.

**Componentes:**
- **Entities**: Modelos de dados
  - `character.py`: Entidade Character
  - `planet.py`: Entidade Planet
  - `starship.py`: Entidade Starship
  - `film.py`: Entidade Film

- **Interfaces**: Contratos abstratos
  - `repository.py`: Interface IRepository
  - `client.py`: Interface IHttpClient
  - `cache.py`: Interface ICache

**Responsabilidades:**
- Definir estrutura de dados
- Estabelecer contratos
- Validações de domínio
- Regras de negócio imutáveis

### 2.4 Infrastructure Layer (Camada de Infraestrutura)

Implementações concretas de acesso a dados e serviços externos.

**Componentes:**
- **HTTP Client**: Comunicação com SWAPI
  - `swapi_client.py`: Cliente HTTP assíncrono

- **Cache**: Armazenamento em cache
  - `memory_cache.py`: Cache em memória
  - `redis_cache.py`: Cache com Redis
  - `cache_factory.py`: Factory para criar instâncias

- **Repositories**: Acesso a dados
  - `base_repository.py`: Classe base com lógica comum
  - `character_repository.py`: Repositório de personagens
  - `planet_repository.py`: Repositório de planetas
  - `starship_repository.py`: Repositório de naves
  - `film_repository.py`: Repositório de filmes

**Responsabilidades:**
- Implementar interfaces de domínio
- Gerenciar conexões externas
- Implementar cache
- Tratar erros de infraestrutura

## 3. Padrões de Design Utilizados

### 3.1 Repository Pattern
Abstrai o acesso a dados, permitindo trocar a fonte sem afetar a lógica de negócio.

```python
# Interface
class IRepository(ABC, Generic[T]):
    async def get_by_id(self, id: str) -> Optional[T]
    async def get_all(...) -> tuple[List[T], int]
    async def search(self, query: str) -> List[T]

# Implementação
class CharacterRepository(BaseRepository[Character]):
    def __init__(self, http_client, cache):
        super().__init__(http_client, cache, "people", Character)
```

### 3.2 Service Layer
Centraliza a lógica de negócio e orquestra operações.

```python
class CharacterService:
    def __init__(self, repository: CharacterRepository):
        self.repository = repository

    async def get_character_by_id(self, id: str) -> Character:
        # Lógica de negócio
        pass
```

### 3.3 Dependency Injection
Injeta dependências via construtor para facilitar testes.

```python
# Injeção via construtor
service = CharacterService(repository)

# Injeção via FastAPI Depends
async def list_characters(
    service: CharacterService = Depends(get_character_service)
):
    pass
```

### 3.4 Factory Pattern
Cria instâncias apropriadas baseado em configuração.

```python
class CacheFactory:
    @staticmethod
    def create_cache() -> ICache:
        if settings.REDIS_URL:
            return RedisCache(settings.REDIS_URL)
        return MemoryCache()
```

### 3.5 DTO Pattern
Separa dados internos de dados transferidos.

```python
class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    page_size: int
    total_pages: int
```

## 4. Fluxo de Requisição

```
1. Cliente HTTP
   ↓
2. FastAPI Route Handler
   ├─ Validação de parâmetros (Pydantic)
   ├─ Autenticação (JWT)
   ↓
3. Service Layer
   ├─ Lógica de negócio
   ├─ Validações
   ↓
4. Repository Layer
   ├─ Verificar cache
   ├─ Se não em cache → HTTP Client
   ├─ Armazenar em cache
   ↓
5. SWAPI API
   ↓
6. Response
   ├─ Serializar (Pydantic)
   ├─ Retornar JSON
   ↓
7. Cliente HTTP
```

## 5. Tratamento de Erros

Exceções customizadas para diferentes cenários:

```python
StarWarsAPIException (base)
├─ ResourceNotFoundError (404)
├─ InvalidFilterError (400)
├─ InvalidSortError (400)
├─ UnauthorizedError (401)
├─ InvalidTokenError (401)
├─ ExpiredTokenError (401)
├─ RateLimitExceededError (429)
├─ ExternalAPIError (502)
└─ CacheError (500)
```

## 6. Cache Strategy

### 6.1 Estratégia de Cache
- **TTL**: 3600 segundos (configurável)
- **Chaves**: `{resource_type}:{operation}:{params}`
- **Invalidação**: Automática por TTL

### 6.2 Implementações
- **Development**: MemoryCache (em memória)
- **Production**: RedisCache (Redis)

### 6.3 Exemplo
```python
# Chave de cache
cache_key = "characters:by_id:1"

# Verificar cache
cached = await cache.get(cache_key)
if cached:
    return cached

# Se não em cache, buscar de SWAPI
data = await http_client.get(url)

# Armazenar em cache
await cache.set(cache_key, data, ttl=3600)
```

## 7. Autenticação e Autorização

### 7.1 JWT (JSON Web Token)
- **Algoritmo**: HS256
- **Expiração**: 24 horas (configurável)
- **Secret**: Armazenado em variável de ambiente

### 7.2 Fluxo
```
1. Cliente faz login
2. Servidor gera JWT
3. Cliente inclui JWT em requisições
4. Middleware valida JWT
5. Requisição processada
```

### 7.3 Implementação
```python
# Criar token
token = JWTHandler.create_token({"sub": "username"})

# Validar token
payload = JWTHandler.verify_token(token)

# Usar em rotas
async def get_resource(
    current_user: str = Depends(get_current_user)
):
    pass
```

## 8. Configuração e Variáveis de Ambiente

```python
# Aplicação
ENVIRONMENT=production
DEBUG=False
LOG_LEVEL=INFO

# SWAPI
SWAPI_BASE_URL=https://swapi.dev/api
SWAPI_TIMEOUT=10

# Cache
CACHE_ENABLED=True
CACHE_TTL=3600
REDIS_URL=redis://localhost:6379/0

# JWT
JWT_SECRET_KEY=your-secret-key
JWT_EXPIRATION_HOURS=24

# GCP
GCP_PROJECT_ID=your-project-id
GCP_ENVIRONMENT=production
```

## 9. Deploy em GCP

### 9.1 Cloud Functions
```bash
gcloud functions deploy starwars-api \
  --runtime python39 \
  --trigger-http \
  --allow-unauthenticated \
  --entry-point starwars_api \
  --set-env-vars ENVIRONMENT=production,REDIS_URL=...
```

### 9.2 API Gateway
Gerencia rotas, autenticação e rate limiting:
- Roteamento de requisições
- Validação de JWT
- Rate limiting por usuário
- Logging e monitoramento

## 10. Escalabilidade

### 10.1 Horizontal Scaling
- Múltiplas instâncias de Cloud Functions
- Load balancing automático
- Cache distribuído (Redis)

### 10.2 Otimizações
- Cache em memória para dados frequentes
- Paginação de resultados
- Índices em Redis
- Compressão de respostas

## 11. Monitoramento e Logging

### 11.1 Cloud Logging
- Logs estruturados
- Níveis: DEBUG, INFO, WARNING, ERROR
- Integração automática com GCP

### 11.2 Métricas
- Tempo de resposta
- Taxa de erro
- Uso de cache
- Requisições por segundo

## 12. Segurança

### 12.1 CORS
- Permite requisições de qualquer origem
- Configurável por ambiente

### 12.2 Rate Limiting
- Implementado no API Gateway
- Limite por usuário/IP
- Respostas com status 429

### 12.3 Validação
- Validação de entrada com Pydantic
- Type hints em todas as funções
- Sanitização de dados

## 13. Testes

### 13.1 Cobertura
- Testes unitários: Services, Repositories
- Testes de integração: Cliente SWAPI, Cache
- Testes de endpoints: Rotas da API

### 13.2 Execução
```bash
# Todos os testes
pytest

# Com cobertura
pytest --cov=src tests/

# Apenas unitários
pytest tests/unit/

# Apenas integração
pytest tests/integration/ -m integration
```

## 14. Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────┐
│                   Cliente HTTP                          │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              API Gateway (GCP)                          │
│  ├─ Roteamento                                          │
│  ├─ Autenticação JWT                                    │
│  ├─ Rate Limiting                                       │
│  └─ Logging                                             │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│          Cloud Functions (FastAPI)                      │
│  ├─ Routes (Characters, Planets, Starships, Films)     │
│  ├─ Services (Business Logic)                          │
│  ├─ Repositories (Data Access)                         │
│  └─ Middleware (Error Handling)                        │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
┌───────▼──────────┐    ┌────────▼────────┐
│   SWAPI API      │    │  Redis Cache    │
│  (External)      │    │  (GCP Memorystore)
└──────────────────┘    └─────────────────┘
```

## 15. Próximos Passos

1. **Implementar GraphQL**: Alternativa a REST
2. **WebSocket**: Atualizações em tempo real
3. **Machine Learning**: Recomendações personalizadas
4. **Analytics**: Dashboard de uso
5. **Mobile App**: Aplicativo nativo
