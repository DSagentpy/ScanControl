# Testes do Scanner Logístico

## Estrutura de Testes

Este diretório contém todos os testes automatizados do projeto.

### Arquivos de Teste

- `test_main.py` - Testes do arquivo principal (main.py)
- `test_produtos.py` - Testes do router de produtos
- `test_recebimentos.py` - Testes do router de recebimentos
- `test_sessao.py` - Testes do router de sessão
- `test_relatorio.py` - Testes do router de relatórios
- `test_schemas.py` - Testes de validação dos schemas Pydantic
- `conftest.py` - Configuração de fixtures compartilhadas

## Executando os Testes

### Executar todos os testes
```bash
pytest
```

### Executar com verbose
```bash
pytest -v
```

### Executar com cobertura
```bash
pytest --cov=app --cov-report=html
```

### Executar um arquivo específico
```bash
pytest tests/test_produtos.py
```

### Executar um teste específico
```bash
pytest tests/test_produtos.py::test_criar_produto_sucesso
```

## Cobertura de Código

A cobertura atual é de **92%**, cobrindo:
- ✅ 100% dos models
- ✅ 100% dos routers (produtos, sessao, relatorio)
- ✅ 100% do router de produtos
- ✅ 80% do router de recebimentos
- ✅ 93% do main.py
- ✅ 90% dos schemas

## Estatísticas

- **Total de testes**: 42
- **Testes passando**: 42 ✅
- **Taxa de sucesso**: 100%
- **Cobertura de código**: 92%

## Tipos de Testes

### Testes de Unidade
- Validação de schemas
- Lógica de negócio

### Testes de Integração
- Endpoints da API
- Interação com banco de dados
- Geração de PDFs

### Testes de Validação
- Campos obrigatórios
- Valores inválidos
- Casos de erro

## Fixtures Disponíveis

- `client` - Cliente FastAPI para testes
- `db_session` - Sessão de banco de dados isolada
- `produto_exemplo` - Dados de exemplo para produto
- `produto_criado` - Produto criado no banco de teste
- `sessao_criada` - Sessão criada no banco de teste

