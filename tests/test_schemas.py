"""
Testes para os schemas Pydantic
"""
import pytest
from pydantic import ValidationError

from app.schemas import ProdutoCreate, RecebimentoCreate, CodigoBarra


def test_produto_create_valido():
    """Testa criação de ProdutoCreate válido"""
    produto = ProdutoCreate(
        codigo="PROD001",
        nome="Produto Teste",
        codigo_barra="7891234567890",
        descricao="Descrição do produto"
    )
    
    assert produto.codigo == "PROD001"
    assert produto.nome == "Produto Teste"
    assert produto.codigo_barra == "7891234567890"
    assert produto.descricao == "Descrição do produto"


def test_produto_create_descricao_opcional():
    """Testa que descrição é opcional"""
    produto = ProdutoCreate(
        codigo="PROD001",
        nome="Produto Teste",
        codigo_barra="7891234567890"
    )
    
    assert produto.descricao == ""


def test_produto_create_codigo_vazio():
    """Testa validação de código vazio"""
    with pytest.raises(ValidationError) as exc_info:
        ProdutoCreate(
            codigo="",
            nome="Produto Teste",
            codigo_barra="7891234567890"
        )
    
    errors = exc_info.value.errors()
    assert any("codigo" in str(error["loc"]) for error in errors)


def test_produto_create_nome_vazio():
    """Testa validação de nome vazio"""
    with pytest.raises(ValidationError) as exc_info:
        ProdutoCreate(
            codigo="PROD001",
            nome="",
            codigo_barra="7891234567890"
        )
    
    errors = exc_info.value.errors()
    assert any("nome" in str(error["loc"]) for error in errors)


def test_produto_create_codigo_barra_vazio():
    """Testa validação de código de barras vazio"""
    with pytest.raises(ValidationError) as exc_info:
        ProdutoCreate(
            codigo="PROD001",
            nome="Produto Teste",
            codigo_barra=""
        )
    
    errors = exc_info.value.errors()
    assert any("codigo_barra" in str(error["loc"]) for error in errors)


def test_produto_create_trim_espacos():
    """Testa que espaços são removidos dos campos"""
    produto = ProdutoCreate(
        codigo="  PROD001  ",
        nome="  Produto Teste  ",
        codigo_barra="  7891234567890  "
    )
    
    assert produto.codigo == "PROD001"
    assert produto.nome == "Produto Teste"
    assert produto.codigo_barra == "7891234567890"


def test_recebimento_create_valido():
    """Testa criação de RecebimentoCreate válido"""
    recebimento = RecebimentoCreate(
        codigo_barra="7891234567890",
        quantidade=5
    )
    
    assert recebimento.codigo_barra == "7891234567890"
    assert recebimento.quantidade == 5


def test_recebimento_create_quantidade_zero():
    """Testa validação de quantidade zero"""
    with pytest.raises(ValidationError) as exc_info:
        RecebimentoCreate(
            codigo_barra="7891234567890",
            quantidade=0
        )
    
    errors = exc_info.value.errors()
    assert any("quantidade" in str(error["loc"]) for error in errors)


def test_recebimento_create_quantidade_negativa():
    """Testa validação de quantidade negativa"""
    with pytest.raises(ValidationError) as exc_info:
        RecebimentoCreate(
            codigo_barra="7891234567890",
            quantidade=-1
        )
    
    errors = exc_info.value.errors()
    assert any("quantidade" in str(error["loc"]) for error in errors)


def test_recebimento_create_codigo_barra_vazio():
    """Testa validação de código de barras vazio"""
    with pytest.raises(ValidationError) as exc_info:
        RecebimentoCreate(
            codigo_barra="",
            quantidade=5
        )
    
    errors = exc_info.value.errors()
    assert any("codigo_barra" in str(error["loc"]) for error in errors)


def test_codigo_barra_valido():
    """Testa criação de CodigoBarra válido"""
    codigo = CodigoBarra(codigo_barra="7891234567890")
    assert codigo.codigo_barra == "7891234567890"


def test_codigo_barra_vazio():
    """Testa validação de código de barras vazio"""
    with pytest.raises(ValidationError) as exc_info:
        CodigoBarra(codigo_barra="")
    
    errors = exc_info.value.errors()
    assert any("codigo_barra" in str(error["loc"]) for error in errors)


def test_codigo_barra_trim_espacos():
    """Testa que espaços são removidos do código de barras"""
    codigo = CodigoBarra(codigo_barra="  7891234567890  ")
    assert codigo.codigo_barra == "7891234567890"

