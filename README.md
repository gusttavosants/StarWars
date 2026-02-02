# Star Wars API

Uma plataforma inovadora dedicada aos fãs de Star Wars, construída com Python, FastAPI e integrada com a API SWAPI.

## 📋 Visão Geral

Esta API permite explorar informações detalhadas sobre personagens, planetas, naves e filmes da saga Star Wars. A plataforma oferece uma experiência rica e interativa com filtros avançados, ordenação e correlações entre dados.

## 🎯 Funcionalidades

- ✅ Consulta de personagens, planetas, naves e filmes
- ✅ Filtros avançados com múltiplos operadores
- ✅ Ordenação de resultados
- ✅ Correlações entre recursos (ex: personagens em um filme)
- ✅ Autenticação JWT
- ✅ Cache inteligente
- ✅ Rate limiting
- ✅ Documentação automática (Swagger)
- ✅ Testes unitários e de integração

## 🏗️ Arquitetura

A aplicação segue os princípios de **Clean Architecture** e **SOLID**:

```
src/
├── config/              # Configurações e constantes
├── domain/              # Entidades e interfaces (regras de negócio)
├── infrastructure/      # Implementações (HTTP, Cache, Repositórios)
├── application/         # Lógica de negócio (Services, DTOs, Segurança)
└── presentation/        # API (Rotas, Middleware)
```

## 🚀 Quick Start

### Pré-requisitos

- Python 3.9+
- pip
- Redis (opcional, para cache em produção)

### Instalação

1. Clone o repositório:
```bash
git clone <seu-repositorio>
cd starwars-api
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
```

5. Execute a aplicação:
```bash
uvicorn src.presentation.main:app --reload
```

A API estará disponível em `http://localhost:8000`

## 📚 Documentação da API

Após iniciar a aplicação, acesse:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Testes

Execute os testes com cobertura:
```bash
pytest --cov=src tests/
```

## 🔐 Autenticação

A API utiliza JWT para autenticação. Obtenha um token:

```bash
curl -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "password"}'
```

Use o token em requisições subsequentes:
```bash
curl -H "Authorization: Bearer <seu-token>" \
  http://localhost:8000/api/characters
```

## 🌐 Deploy em GCP

### Cloud Functions

1. Prepare o ambiente:
```bash
gcloud functions deploy starwars-api \
  --runtime python39 \
  --trigger-http \
  --allow-unauthenticated \
  --entry-point starwars_api
```

2. Configure o API Gateway para gerenciar rotas e autenticação.

## 📝 Padrões de Desenvolvimento

- **Clean Code**: Nomes descritivos, funções pequenas, sem magic numbers
- **SOLID**: Responsabilidade única, aberto/fechado, substituição de Liskov, segregação de interface, inversão de dependência
- **Type Hints**: Todas as funções com type hints
- **Docstrings**: Documentação em classes e métodos públicos
- **Testes**: Cobertura mínima 80%

## 📦 Estrutura de Commits

```
feat: adiciona nova funcionalidade
fix: corrige bug
docs: atualiza documentação
test: adiciona testes
refactor: refatora código
```

## 📄 Licença

MIT

## 👥 Contribuidores

- PowerOfData Team

## 📞 Suporte

Para dúvidas ou sugestões, abra uma issue no repositório.
