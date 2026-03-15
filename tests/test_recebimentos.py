"""
Testes para o router de recebimentos
"""
import pytest
from fastapi import status


def test_verificar_produto_cadastrado(client, produto_criado):
    """Testa verificação de produto cadastrado"""
    codigo_barra = produto_criado["codigo_barra"]
    
    response = client.post(
        "/recebimentos/verificar",
        json={"codigo_barra": codigo_barra}
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["cadastrado"] is True
    assert data["nome"] == produto_criado["nome"]


def test_verificar_produto_nao_cadastrado(client):
    """Testa verificação de produto não cadastrado"""
    response = client.post(
        "/recebimentos/verificar",
        json={"codigo_barra": "9999999999999"}
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["cadastrado"] is False


def test_verificar_codigo_barra_vazio(client):
    """Testa validação de código de barras vazio"""
    response = client.post(
        "/recebimentos/verificar",
        json={"codigo_barra": ""}
    )
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_salvar_recebimento_sucesso(client, produto_criado, sessao_criada):
    """Testa salvamento de recebimento com sucesso"""
    sessao_id = sessao_criada["id"]
    codigo_barra = produto_criado["codigo_barra"]
    
    response = client.post(
        f"/recebimentos/salvar/{sessao_id}",
        json={
            "codigo_barra": codigo_barra,
            "quantidade": 5
        }
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["quantidade_total"] == 5


def test_salvar_recebimento_quantidade_zero(client, produto_criado, sessao_criada):
    """Testa que quantidade zero não é permitida"""
    sessao_id = sessao_criada["id"]
    codigo_barra = produto_criado["codigo_barra"]
    
    response = client.post(
        f"/recebimentos/salvar/{sessao_id}",
        json={
            "codigo_barra": codigo_barra,
            "quantidade": 0
        }
    )
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_salvar_recebimento_quantidade_negativa(client, produto_criado, sessao_criada):
    """Testa que quantidade negativa não é permitida"""
    sessao_id = sessao_criada["id"]
    codigo_barra = produto_criado["codigo_barra"]
    
    response = client.post(
        f"/recebimentos/salvar/{sessao_id}",
        json={
            "codigo_barra": codigo_barra,
            "quantidade": -1
        }
    )
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_salvar_recebimento_produto_inexistente(client, sessao_criada):
    """Testa salvamento com produto inexistente"""
    sessao_id = sessao_criada["id"]
    
    response = client.post(
        f"/recebimentos/salvar/{sessao_id}",
        json={
            "codigo_barra": "9999999999999",
            "quantidade": 5
        }
    )
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "não encontrado" in response.json()["detail"].lower()


def test_salvar_recebimento_sessao_inexistente(client, produto_criado):
    """Testa salvamento com sessão inexistente"""
    codigo_barra = produto_criado["codigo_barra"]
    
    response = client.post(
        "/recebimentos/salvar/99999",
        json={
            "codigo_barra": codigo_barra,
            "quantidade": 5
        }
    )
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "não encontrada" in response.json()["detail"].lower()


def test_salvar_recebimentos_multiplos(client, produto_criado, sessao_criada):
    """Testa salvamento de múltiplos recebimentos do mesmo produto"""
    sessao_id = sessao_criada["id"]
    codigo_barra = produto_criado["codigo_barra"]
    
    # Primeiro recebimento
    response1 = client.post(
        f"/recebimentos/salvar/{sessao_id}",
        json={"codigo_barra": codigo_barra, "quantidade": 3}
    )
    assert response1.status_code == status.HTTP_200_OK
    assert response1.json()["quantidade_total"] == 3
    
    # Segundo recebimento
    response2 = client.post(
        f"/recebimentos/salvar/{sessao_id}",
        json={"codigo_barra": codigo_barra, "quantidade": 2}
    )
    assert response2.status_code == status.HTTP_200_OK
    assert response2.json()["quantidade_total"] == 5


def test_lista_produtos_sessao(client, produto_criado, sessao_criada):
    """Testa listagem de produtos de uma sessão"""
    sessao_id = sessao_criada["id"]
    codigo_barra = produto_criado["codigo_barra"]
    
    # Adiciona recebimento
    client.post(
        f"/recebimentos/salvar/{sessao_id}",
        json={"codigo_barra": codigo_barra, "quantidade": 10}
    )
    
    # Lista produtos
    response = client.get(f"/recebimentos/lista/{sessao_id}")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["nome"] == produto_criado["nome"]
    assert data[0]["total"] == 10


def test_lista_produtos_sessao_vazia(client, sessao_criada):
    """Testa listagem de produtos de sessão vazia"""
    sessao_id = sessao_criada["id"]
    
    response = client.get(f"/recebimentos/lista/{sessao_id}")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0

