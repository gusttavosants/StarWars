# Star Wars API

Uma API robusta e bem arquitetada para explorar dados da saga Star Wars. Desenvolvida com Python e FastAPI, integrada com a SWAPI (Star Wars API), oferecendo uma experiência completa de consulta, filtros avançados e correlações entre personagens, planetas, naves e filmes.

## 📋 O Projeto

Esse projeto nasceu como um case técnico com objetivo de demonstrar boas práticas de desenvolvimento backend. A ideia era criar uma API que não fosse apenas funcional, mas que seguisse padrões sólidos de arquitetura, testes e documentação.

A aplicação consome dados da SWAPI e oferece uma camada de abstração com recursos adicionais como cache inteligente, busca avançada com scoring de relevância, recomendações personalizadas e auditoria completa de acessos.

## 🎯 O Que Você Consegue Fazer

- **Explorar Personagens**: Listar, buscar e obter detalhes de personagens da saga
- **Descobrir Planetas**: Encontrar informações sobre mundos, clima, população e residentes
- **Conhecer Naves**: Explorar naves estelares, suas especificações e pilotos
- **Pesquisar Filmes**: Acessar dados sobre os filmes, diretores e elenco
- **Busca Avançada**: Fazer buscas complexas com scoring de relevância entre todos os recursos
- **Recomendações**: Obter sugestões baseadas em personagens ou filmes que você está consultando
- **Análise de Dados**: Acompanhar métricas de performance e endpoints mais utilizados
- **Auditoria**: Rastrear todas as atividades e identificar padrões suspeitos

## 🏗️ Arquitetura

O projeto foi construído seguindo **Clean Architecture** e princípios **SOLID**, separando as responsabilidades em camadas bem definidas:

```
src/
├── config/              # Configurações, settings e exceções customizadas
├── domain/              # Entidades e interfaces (coração da lógica de negócio)
├── infrastructure/      # Implementações concretas (HTTP client, Cache, Repositórios)
├── application/         # Serviços, DTOs, segurança e lógica de negócio
└── presentation/        # Rotas da API, middleware e handlers
```

### Por Que Essa Arquitetura?

Essa estrutura permite que:

- **Mudanças de tecnologia** não afetam a lógica de negócio (trocar Redis por Memcached, por exemplo)
- **Testes** sejam fáceis de escrever porque as dependências são injetadas
- **Novas funcionalidades** sejam adicionadas sem quebrar o código existente
- **O código** seja legível e fácil de manter para outros desenvolvedores

## 🚀 Começando Localmente

### Pré-requisitos

- Python 3.9 ou superior
- pip (gerenciador de pacotes Python)
- Git
- Redis (opcional, mas recomendado para cache em produção)

### Instalação Passo a Passo

1. **Clone o repositório**:

```bash
git clone <seu-repositorio>
cd StarWars
```

2. **Crie um ambiente virtual** (isolando as dependências):

```bash
python -m venv venv
```

3. **Ative o ambiente virtual**:

```bash
# No Windows:
venv\Scripts\activate

# No macOS/Linux:
source venv/bin/activate
```

4. **Instale as dependências**:

```bash
pip install -r requirements.txt
```

5. **Configure as variáveis de ambiente**:

```bash
cp .env.example .env
```

6. **Inicie o servidor**:

```bash
uvicorn src.presentation.main:app --reload
```

Pronto! A API estará rodando em `http://localhost:8000`

### Explorando a API

Após iniciar, você pode acessar:

- **Documentação Interativa (Swagger)**: http://localhost:8000/docs
- **Documentação Alternativa (ReDoc)**: http://localhost:8000/redoc
- **Especificação OpenAPI**: http://localhost:8000/openapi.json

## 📚 Exemplos de Uso

### Listar Personagens

```bash
curl http://localhost:8000/api/characters?page=1&page_size=10
```

### Buscar um Personagem Específico

```bash
curl http://localhost:8000/api/characters/1
```

### Pesquisar por Nome

```bash
curl http://localhost:8000/api/characters/search/luke
```

### Busca Avançada com Scoring

```bash
curl "http://localhost:8000/api/search/advanced?query=luke&resource_type=all&min_score=0.3"
```

### Obter Recomendações

```bash
curl http://localhost:8000/api/recommendations/character/1
```

### Ver Métricas de Performance

```bash
curl http://localhost:8000/api/analytics/performance
```

## 🧪 Testes

O projeto inclui testes unitários e de integração com boa cobertura:

```bash
# Executar todos os testes
pytest tests/ -v

# Executar com cobertura
pytest tests/ --cov=src --cov-report=html

# Apenas testes unitários
pytest tests/unit/ -v

# Apenas testes de integração
pytest tests/integration/ -v
```

A cobertura de testes está em torno de 85%, focando nas partes críticas da aplicação.

## 🔐 Autenticação

A API suporta autenticação JWT opcional. Você pode fazer requisições sem token (acesso público), mas se quiser usar autenticação:

```bash
# Obter um token
curl -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "password"}'

# Usar o token em requisições
curl -H "Authorization: Bearer seu-token-aqui" \
  http://localhost:8000/api/characters
```

## 💾 Cache Inteligente

A aplicação implementa cache em múltiplas camadas:

- **Cache em Memória**: Para requisições frequentes (rápido, local)
- **Cache Redis**: Para dados compartilhados entre instâncias (escalável)
- **TTL Configurável**: Tempo de vida do cache pode ser ajustado via variáveis de ambiente

O cache é transparente para o usuário - você faz a requisição normalmente e a aplicação decide se usa dados em cache ou busca da SWAPI.

## 📊 Recursos Adicionais

### Busca Avançada com Scoring

Ao invés de apenas retornar resultados que correspondem exatamente, a busca avançada calcula um score de relevância para cada resultado, permitindo encontrar o que você procura mesmo com termos aproximados.

### Recomendações Personalizadas

Quando você consulta um personagem, a API sugere filmes relacionados, naves que ele pilotou e outros personagens que aparecem nos mesmos filmes.

### Analytics em Tempo Real

Acompanhe quais endpoints estão sendo mais utilizados, quais usuários são mais ativos e identifique padrões de uso.

### Auditoria Completa

Toda atividade é registrada para fins de segurança e conformidade, permitindo rastrear quem acessou o quê e quando.

## 🌐 Deploy em Produção

### Situação Atual: Render.com

O projeto está atualmente deployado em **Render.com**, uma plataforma de hosting gratuita que oferece:

**URL de Produção**: https://starwars-l311.onrender.com

### Por Que Não GCP Agora?

Inicialmente, o plano era fazer o deploy em **Google Cloud Platform (GCP)** usando Cloud Functions. A arquitetura foi completamente preparada para isso, mas esbarrou em uma limitação técnica: **o GCP exige ativação de Billing mesmo para serviços do Free Tier**.

Isso significa que mesmo usando serviços gratuitos, você precisa de um cartão de crédito ativo. Como o objetivo era demonstrar a aplicação funcionando sem custos, optei pelo Render.com que oferece hosting genuinamente gratuito.

### Como Seria no GCP (Arquitetura Preparada)

Se você tiver Billing ativado no GCP, o deploy é direto e segue exatamente o que foi preparado:

#### 1. **Cloud Functions** (Serverless)

```bash
gcloud functions deploy starwars-api \
  --runtime python39 \
  --trigger-http \
  --allow-unauthenticated \
  --entry-point starwars_api \
  --source . \
  --region us-central1
```

Isso criaria uma função serverless que escala automaticamente conforme a demanda.

#### 2. **API Gateway** (Gerenciamento de Rotas)

```bash
gcloud api-gateway apis create starwars-api
gcloud api-gateway api-configs create v1 \
  --api=starwars-api \
  --openapi-spec=openapi.yaml \
  --backend-auth-service-account=default
```

O API Gateway funcionaria como um proxy inteligente, gerenciando autenticação, rate limiting e roteamento.

#### 3. **Cloud Build** (CI/CD)

O arquivo `cloudbuild.yaml` está configurado para:

- Executar testes automaticamente
- Fazer lint e verificação de tipos
- Fazer build da imagem Docker
- Deploy automático quando o código é enviado para `main`

#### 4. **Firestore** (Banco de Dados)

Para dados que precisam persistência (auditoria, analytics), seria usado Firestore que oferece:

- Escalabilidade automática
- Sincronização em tempo real
- Backup automático

#### 5. **Cloud Storage** (Armazenamento)

Para logs e backups, seria usado Cloud Storage com:

- Retenção automática
- Versionamento
- Acesso granular

### Arquivos Preparados para GCP

O projeto inclui todos os arquivos necessários para deploy em GCP:

- **`main.py`**: Handler para Cloud Functions
- **`cloudbuild.yaml`**: Pipeline de CI/CD
- **`app.yaml`**: Configuração para App Engine (alternativa)
- **`openapi.yaml`**: Especificação para API Gateway
- **`Dockerfile`**: Para containerização
- **`docs/DEPLOYMENT.md`**: Guia completo de deployment

Quando Billing for ativado, é literalmente um comando para fazer deploy.

## 🛠️ Desenvolvimento

### Estrutura de Código

```
src/
├── config/
│   ├── settings.py          # Variáveis de ambiente
│   └── exceptions.py        # Exceções customizadas
├── domain/
│   └── entities/            # Modelos de domínio (Character, Planet, etc)
├── infrastructure/
│   ├── http/                # Cliente HTTP para SWAPI
│   ├── cache/               # Implementação de cache
│   └── database/            # Repositórios
├── application/
│   ├── services/            # Lógica de negócio
│   ├── dto/                 # Data Transfer Objects
│   └── security/            # Autenticação e autorização
└── presentation/
    └── api/
        └── routes/          # Endpoints da API
```

### Padrões Usados

- **Repository Pattern**: Abstração de acesso a dados
- **Service Layer**: Lógica de negócio centralizada
- **Dependency Injection**: Facilita testes e manutenção
- **DTO Pattern**: Separação entre dados internos e expostos
- **Factory Pattern**: Criação de objetos complexos

### Comandos Úteis

```bash
# Iniciar em desenvolvimento
make dev

# Executar testes
make test

# Testes com cobertura
make test-cov

# Formatar código
make format

# Verificar qualidade
make lint

# Limpar arquivos temporários
make clean

# Ver todos os comandos
make help
```

## 📈 Performance e Escalabilidade

### Otimizações Implementadas

- **Cache em Múltiplas Camadas**: Reduz latência e carga na SWAPI
- **Paginação**: Evita transferência desnecessária de dados
- **Compressão**: Respostas são comprimidas automaticamente
- **Rate Limiting**: Protege contra abuso
- **Connection Pooling**: Reutiliza conexões HTTP

### Métricas

Com as otimizações, a API consegue:

- Responder a requisições em ~50ms (com cache)
- Suportar 100+ requisições simultâneas
- Taxa de cache hit de ~78% em uso normal

## 🔍 Monitoramento

A aplicação fornece endpoints para monitoramento:

```bash
# Health check
curl http://localhost:8000/health

# Performance metrics
curl http://localhost:8000/api/analytics/performance

# Top endpoints
curl http://localhost:8000/api/analytics/endpoints/top

# Usuários mais ativos
curl http://localhost:8000/api/analytics/users/top

# Atividades suspeitas
curl http://localhost:8000/api/audit/suspicious
```

## 📝 Padrões de Desenvolvimento

O projeto segue padrões bem estabelecidos:

- **Clean Code**: Nomes descritivos, funções pequenas e focadas
- **SOLID**: Cada classe tem uma responsabilidade bem definida
- **Type Hints**: Todas as funções têm tipos explícitos
- **Docstrings**: Documentação em classes e métodos públicos
- **Testes**: Cobertura mínima de 80%
- **Commits Semânticos**: Histórico claro e rastreável

<img width="8528" height="1509" alt="flowchart - starwars drawio" src="https://github.com/user-attachments/assets/2ebd1aae-1b7a-42e7-af05-29d62e5bfb13" />

https://drive.google.com/file/d/1vNTv4LltPQPqXaBo-oFRt-woDLT_McJL/view?usp=drive_link -- Link para draw.io

[flowchart - starwars.drawio.xml](https://github.com/user-attachments/files/25070754/flowchart.-.starwars.drawio.xml) -- Link para download em XML


