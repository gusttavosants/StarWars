# Documentação da API - Star Wars

## Base URL

```
https://your-api-domain.com/api
```

## Autenticação

Todas as rotas (exceto `/health`) requerem autenticação via JWT.

**Header:**
```
Authorization: Bearer <seu-token-jwt>
```

## Endpoints

### Characters (Personagens)

#### 1. Listar Personagens

```http
GET /api/characters
```

**Parâmetros de Query:**
- `page` (int, opcional): Número da página (padrão: 1)
- `page_size` (int, opcional): Itens por página (padrão: 10, máximo: 100)
- `sort_by` (string, opcional): Campo para ordenar (ex: name, height, mass)
- `sort_order` (string, opcional): Ordem (asc ou desc, padrão: asc)
- `search` (string, opcional): Termo de busca por nome

**Exemplo:**
```bash
curl -H "Authorization: Bearer <token>" \
  "https://api.example.com/api/characters?page=1&page_size=10&sort_by=name&sort_order=asc"
```

**Resposta (200):**
```json
{
  "items": [
    {
      "name": "Luke Skywalker",
      "height": "172",
      "mass": "77",
      "hair_color": "blond",
      "skin_color": "fair",
      "eye_color": "blue",
      "birth_year": "19BBY",
      "gender": "male",
      "homeworld": "https://swapi.dev/api/planets/1/",
      "films": ["https://swapi.dev/api/films/1/"],
      "species": ["https://swapi.dev/api/species/1/"],
      "vehicles": ["https://swapi.dev/api/vehicles/14/"],
      "starships": ["https://swapi.dev/api/starships/12/"],
      "url": "https://swapi.dev/api/people/1/"
    }
  ],
  "total": 82,
  "page": 1,
  "page_size": 10,
  "total_pages": 9
}
```

#### 2. Obter Personagem por ID

```http
GET /api/characters/{character_id}
```

**Parâmetros:**
- `character_id` (string): ID do personagem

**Exemplo:**
```bash
curl -H "Authorization: Bearer <token>" \
  "https://api.example.com/api/characters/1"
```

**Resposta (200):**
```json
{
  "name": "Luke Skywalker",
  "height": "172",
  "mass": "77",
  "hair_color": "blond",
  "skin_color": "fair",
  "eye_color": "blue",
  "birth_year": "19BBY",
  "gender": "male",
  "homeworld": "https://swapi.dev/api/planets/1/",
  "films": ["https://swapi.dev/api/films/1/"],
  "species": ["https://swapi.dev/api/species/1/"],
  "vehicles": ["https://swapi.dev/api/vehicles/14/"],
  "starships": ["https://swapi.dev/api/starships/12/"],
  "url": "https://swapi.dev/api/people/1/"
}
```

#### 3. Buscar Personagens

```http
GET /api/characters/search/{query}
```

**Parâmetros:**
- `query` (string): Termo de busca (mínimo 2 caracteres)

**Exemplo:**
```bash
curl -H "Authorization: Bearer <token>" \
  "https://api.example.com/api/characters/search/luke"
```

**Resposta (200):**
```json
[
  {
    "name": "Luke Skywalker",
    ...
  }
]
```

#### 4. Personagens de um Filme

```http
GET /api/characters/film/{film_id}/characters
```

**Parâmetros:**
- `film_id` (string): ID do filme

**Exemplo:**
```bash
curl -H "Authorization: Bearer <token>" \
  "https://api.example.com/api/characters/film/1/characters"
```

**Resposta (200):**
```json
[
  {
    "name": "Luke Skywalker",
    ...
  },
  {
    "name": "C-3PO",
    ...
  }
]
```

#### 5. Residentes de um Planeta

```http
GET /api/characters/planet/{planet_id}/residents
```

**Parâmetros:**
- `planet_id` (string): ID do planeta

**Exemplo:**
```bash
curl -H "Authorization: Bearer <token>" \
  "https://api.example.com/api/characters/planet/1/residents"
```

**Resposta (200):**
```json
[
  {
    "name": "Luke Skywalker",
    ...
  }
]
```

---

### Planets (Planetas)

#### 1. Listar Planetas

```http
GET /api/planets
```

**Parâmetros de Query:**
- `page` (int, opcional): Número da página
- `page_size` (int, opcional): Itens por página
- `sort_by` (string, opcional): Campo para ordenar (ex: name, diameter, population)
- `sort_order` (string, opcional): Ordem (asc ou desc)
- `search` (string, opcional): Termo de busca

**Resposta (200):**
```json
{
  "items": [
    {
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
      "url": "https://swapi.dev/api/planets/1/"
    }
  ],
  "total": 60,
  "page": 1,
  "page_size": 10,
  "total_pages": 6
}
```

#### 2. Obter Planeta por ID

```http
GET /api/planets/{planet_id}
```

#### 3. Buscar Planetas

```http
GET /api/planets/search/{query}
```

#### 4. Planetas de um Filme

```http
GET /api/planets/film/{film_id}/planets
```

#### 5. Planetas por Clima

```http
GET /api/planets/climate/{climate}
```

**Parâmetros:**
- `climate` (string): Tipo de clima (ex: arid, temperate, tropical)

---

### Starships (Naves Estelares)

#### 1. Listar Naves

```http
GET /api/starships
```

**Parâmetros de Query:**
- `page` (int, opcional): Número da página
- `page_size` (int, opcional): Itens por página
- `sort_by` (string, opcional): Campo para ordenar (ex: name, length, cost_in_credits)
- `sort_order` (string, opcional): Ordem (asc ou desc)
- `search` (string, opcional): Termo de busca

**Resposta (200):**
```json
{
  "items": [
    {
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
      "url": "https://swapi.dev/api/starships/12/"
    }
  ],
  "total": 37,
  "page": 1,
  "page_size": 10,
  "total_pages": 4
}
```

#### 2. Obter Nave por ID

```http
GET /api/starships/{starship_id}
```

#### 3. Buscar Naves

```http
GET /api/starships/search/{query}
```

#### 4. Naves de um Filme

```http
GET /api/starships/film/{film_id}/starships
```

#### 5. Naves por Classe

```http
GET /api/starships/class/{starship_class}
```

**Parâmetros:**
- `starship_class` (string): Classe da nave (ex: Starfighter, Transport)

#### 6. Naves de um Piloto

```http
GET /api/starships/pilot/{pilot_id}/starships
```

**Parâmetros:**
- `pilot_id` (string): ID do piloto

---

### Films (Filmes)

#### 1. Listar Filmes

```http
GET /api/films
```

**Parâmetros de Query:**
- `page` (int, opcional): Número da página
- `page_size` (int, opcional): Itens por página
- `sort_by` (string, opcional): Campo para ordenar (ex: title, episode_id, release_date)
- `sort_order` (string, opcional): Ordem (asc ou desc)
- `search` (string, opcional): Termo de busca

**Resposta (200):**
```json
{
  "items": [
    {
      "title": "A New Hope",
      "episode_id": 4,
      "opening_crawl": "It is a period of civil war...",
      "director": "George Lucas",
      "producer": "Gary Kurtz, Rick McCallum",
      "release_date": "1977-05-25",
      "characters": ["https://swapi.dev/api/people/1/"],
      "planets": ["https://swapi.dev/api/planets/1/"],
      "starships": ["https://swapi.dev/api/starships/12/"],
      "vehicles": ["https://swapi.dev/api/vehicles/14/"],
      "species": ["https://swapi.dev/api/species/1/"],
      "url": "https://swapi.dev/api/films/1/"
    }
  ],
  "total": 6,
  "page": 1,
  "page_size": 10,
  "total_pages": 1
}
```

#### 2. Obter Filme por ID

```http
GET /api/films/{film_id}
```

#### 3. Buscar Filmes

```http
GET /api/films/search/{query}
```

#### 4. Filmes por Diretor

```http
GET /api/films/director/{director}
```

**Parâmetros:**
- `director` (string): Nome do diretor

#### 5. Filmes de um Personagem

```http
GET /api/films/character/{character_id}/films
```

#### 6. Filmes de um Planeta

```http
GET /api/films/planet/{planet_id}/films
```

#### 7. Filmes de uma Nave

```http
GET /api/films/starship/{starship_id}/films
```

---

## Códigos de Status HTTP

| Código | Descrição |
|--------|-----------|
| 200 | Sucesso |
| 400 | Requisição inválida |
| 401 | Não autorizado |
| 404 | Recurso não encontrado |
| 429 | Limite de requisições excedido |
| 500 | Erro interno do servidor |
| 502 | Gateway inválido |
| 504 | Timeout |

---

## Formato de Erro

```json
{
  "error": "ResourceNotFoundError",
  "message": "Personagem com ID '999' não encontrado",
  "status_code": 404
}
```

---

## Exemplos de Uso

### Python

```python
import requests

# Configurar token
headers = {
    "Authorization": "Bearer <seu-token-jwt>"
}

# Listar personagens
response = requests.get(
    "https://api.example.com/api/characters",
    params={"page": 1, "page_size": 10},
    headers=headers
)
characters = response.json()

# Obter personagem específico
response = requests.get(
    "https://api.example.com/api/characters/1",
    headers=headers
)
luke = response.json()

# Buscar personagens
response = requests.get(
    "https://api.example.com/api/characters/search/luke",
    headers=headers
)
results = response.json()
```

### JavaScript/Node.js

```javascript
const token = '<seu-token-jwt>';

// Listar personagens
fetch('https://api.example.com/api/characters?page=1&page_size=10', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
})
.then(response => response.json())
.then(data => console.log(data));

// Obter personagem específico
fetch('https://api.example.com/api/characters/1', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
})
.then(response => response.json())
.then(luke => console.log(luke));
```

### cURL

```bash
# Listar personagens
curl -H "Authorization: Bearer <token>" \
  "https://api.example.com/api/characters?page=1&page_size=10"

# Obter personagem específico
curl -H "Authorization: Bearer <token>" \
  "https://api.example.com/api/characters/1"

# Buscar personagens
curl -H "Authorization: Bearer <token>" \
  "https://api.example.com/api/characters/search/luke"
```

---

## Rate Limiting

A API implementa rate limiting para proteger contra abuso:

- **Limite**: 100 requisições por hora
- **Header de Resposta**: `X-RateLimit-Remaining`
- **Status 429**: Quando limite é excedido

---

## Paginação

Todas as listagens suportam paginação:

```json
{
  "items": [...],
  "total": 82,
  "page": 1,
  "page_size": 10,
  "total_pages": 9
}
```

**Cálculo de páginas:**
```
total_pages = ceil(total / page_size)
```

---

## Ordenação

Suporte a ordenação em qualquer campo:

```bash
# Ordenar por nome (ascendente)
GET /api/characters?sort_by=name&sort_order=asc

# Ordenar por altura (descendente)
GET /api/characters?sort_by=height&sort_order=desc
```

---

## Busca

Busca por termo em campos de texto:

```bash
# Buscar personagem
GET /api/characters/search/luke

# Buscar planeta
GET /api/planets/search/tatooine

# Buscar filme
GET /api/films/search/hope
```

---

## Health Check

```http
GET /health
```

**Resposta (200):**
```json
{
  "status": "healthy",
  "app": "Star Wars API",
  "version": "1.0.0"
}
```

---

## Changelog

### v1.0.0 (2024-01-30)
- Lançamento inicial
- Endpoints para Characters, Planets, Starships, Films
- Autenticação JWT
- Cache inteligente
- Documentação completa
