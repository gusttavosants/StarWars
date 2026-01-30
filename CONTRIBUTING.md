# Guia de Contribuição - Star Wars API

## Como Contribuir

Obrigado por seu interesse em contribuir para a Star Wars API! Este documento descreve como fazer isso.

## Código de Conduta

Todos os contribuidores devem seguir nosso código de conduta:
- Ser respeitoso com outros contribuidores
- Aceitar críticas construtivas
- Focar no que é melhor para a comunidade
- Mostrar empatia com outros membros da comunidade

## Como Começar

### 1. Fork o Repositório

```bash
git clone https://github.com/seu-usuario/starwars-api.git
cd starwars-api
```

### 2. Criar Branch para Feature

```bash
git checkout -b feature/sua-feature
```

### 3. Fazer Alterações

Siga os padrões de código do projeto:
- Use type hints em todas as funções
- Escreva docstrings em classes e métodos públicos
- Mantenha linhas com máximo 100 caracteres
- Siga PEP 8

### 4. Adicionar Testes

```bash
# Criar testes para sua feature
pytest tests/unit/test_sua_feature.py -v

# Verificar cobertura
pytest --cov=src tests/
```

### 5. Executar Linting

```bash
# Formatar código
black src/ tests/

# Verificar estilo
flake8 src/ tests/ --max-line-length=100

# Type checking
mypy src/ --ignore-missing-imports
```

### 6. Fazer Commit

```bash
git add .
git commit -m "feat: descrição clara da feature"
```

**Padrão de Commits:**
- `feat:` - Nova funcionalidade
- `fix:` - Correção de bug
- `docs:` - Atualização de documentação
- `test:` - Adição de testes
- `refactor:` - Refatoração de código
- `style:` - Mudanças de estilo (sem lógica)
- `chore:` - Atualização de dependências

### 7. Push e Pull Request

```bash
git push origin feature/sua-feature
```

Abra um Pull Request no GitHub com:
- Descrição clara da mudança
- Referência a issues relacionadas
- Screenshots (se aplicável)
- Checklist de testes

## Padrões de Código

### Type Hints

```python
# ✅ Correto
async def get_character(self, character_id: str) -> Character:
    """Obtém um personagem pelo ID."""
    pass

# ❌ Incorreto
async def get_character(self, character_id):
    pass
```

### Docstrings

```python
# ✅ Correto
def calculate_total_pages(total: int, page_size: int) -> int:
    """
    Calcula o número total de páginas.

    Args:
        total: Número total de itens
        page_size: Itens por página

    Returns:
        Número total de páginas

    Example:
        >>> calculate_total_pages(100, 10)
        10
    """
    return (total + page_size - 1) // page_size

# ❌ Incorreto
def calculate_total_pages(total, page_size):
    # Calcula páginas
    return (total + page_size - 1) // page_size
```

### Tratamento de Erros

```python
# ✅ Correto
try:
    result = await self.repository.get_by_id(resource_id)
    if not result:
        raise ResourceNotFoundError("Resource", resource_id)
    return result
except ExternalAPIError as e:
    logger.error(f"Erro ao acessar API: {str(e)}")
    raise

# ❌ Incorreto
try:
    return await self.repository.get_by_id(resource_id)
except:
    pass
```

### Testes

```python
# ✅ Correto
@pytest.mark.asyncio
async def test_get_character_by_id_success(service, mock_repository):
    """Testa obtenção de personagem com sucesso."""
    # Arrange
    expected = Character(name="Luke", height="172")
    mock_repository.get_by_id.return_value = expected

    # Act
    result = await service.get_character_by_id("1")

    # Assert
    assert result.name == "Luke"
    mock_repository.get_by_id.assert_called_once_with("1")

# ❌ Incorreto
def test_get_character():
    # Teste sem estrutura clara
    pass
```

## Estrutura de Diretórios

Ao adicionar novos arquivos, siga a estrutura:

```
src/
├── config/              # Configurações
├── domain/
│   ├── entities/       # Novas entidades aqui
│   └── interfaces/     # Novas interfaces aqui
├── infrastructure/
│   ├── http/          # Clientes HTTP
│   ├── cache/         # Implementações de cache
│   └── database/
│       └── repositories/  # Novos repositórios aqui
├── application/
│   ├── services/      # Novos serviços aqui
│   ├── dto/          # DTOs
│   └── security/     # Segurança
└── presentation/
    └── api/
        ├── routes/   # Novas rotas aqui
        └── middleware/
```

## Checklist para Pull Request

- [ ] Código segue os padrões do projeto
- [ ] Testes foram adicionados/atualizados
- [ ] Cobertura de testes >= 80%
- [ ] Documentação foi atualizada
- [ ] Linting passa (black, flake8, mypy)
- [ ] Commits seguem o padrão
- [ ] Sem conflitos com main
- [ ] Descrição clara do PR

## Processo de Review

1. **Submeter PR**: Descrever mudanças claramente
2. **Review**: Mantenedores revisarão o código
3. **Feedback**: Responder a comentários e fazer ajustes
4. **Aprovação**: PR será aprovado após feedback positivo
5. **Merge**: Mantenedor fará merge para main

## Reportar Bugs

Ao reportar bugs, inclua:
- Descrição clara do problema
- Passos para reproduzir
- Comportamento esperado
- Comportamento atual
- Versão do Python
- Logs de erro

**Exemplo:**
```
Título: Erro ao buscar personagem com ID inválido

Descrição:
Ao tentar obter um personagem com ID "999", a API retorna erro 500
em vez de 404.

Passos para reproduzir:
1. Fazer requisição GET /api/characters/999
2. Observar resposta

Comportamento esperado:
Status 404 com mensagem "Personagem não encontrado"

Comportamento atual:
Status 500 com mensagem "Erro interno do servidor"

Logs:
[ERROR] ResourceNotFoundError: Personagem com ID '999' não encontrado
```

## Sugerir Features

Ao sugerir features, descreva:
- Caso de uso
- Benefício para usuários
- Exemplos de uso
- Possíveis implementações

**Exemplo:**
```
Título: Adicionar filtro por gênero em personagens

Descrição:
Seria útil poder filtrar personagens por gênero para análises específicas.

Caso de uso:
Um usuário quer analisar quantos personagens femininos aparecem em cada filme.

Exemplo de uso:
GET /api/characters?gender=female

Benefício:
Facilita análises de dados e melhora experiência do usuário.
```

## Dúvidas?

- Abrir issue para discussão
- Contactar mantenedores
- Verificar documentação existente

## Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a mesma licença do projeto (MIT).

## Agradecimentos

Obrigado por contribuir para tornar a Star Wars API melhor! 🚀
