"""
Testes para o router de produtos
"""
import pytest
from fastapi import status


def test_criar_produto_sucesso(client, produto_exemplo):
    """Testa criação de produto com sucesso"""
    response = client.post("/produtos", json=produto_exemplo)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["nome"] == produto_exemplo["nome"]
    assert data["codigo_barra"] == produto_exemplo["codigo_barra"]
    assert "id" in data


def test_criar_produto_duplicado(client, produto_exemplo):
    """Testa que não é possível criar produto com código de barras duplicado"""
    response1 = client.post("/produtos", json=produto_exemplo)
    assert response1.status_code == status.HTTP_201_CREATED

    response2 = client.post("/produtos", json=produto_exemplo)
    assert response2.status_code == status.HTTP_400_BAD_REQUEST
    assert "já cadastrado" in response2.json()["detail"].lower()


def test_criar_produto_campos_vazios(client):
    """Testa validação de campos obrigatórios"""
    produto_invalido = {
        "codigo": "",
        "nome": "",
        "codigo_barra": "",
        "descricao": ""
    }
    response = client.post("/produtos", json=produto_invalido)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_criar_produto_campos_faltando(client):
    """Testa que campos obrigatórios são necessários"""
    produto_incompleto = {"codigo": "PROD001"}
    response = client.post("/produtos", json=produto_incompleto)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_criar_produto_descricao_opcional(client):
    """Testa que descrição é opcional"""
    produto_sem_descricao = {
        "codigo": "PROD002",
        "nome": "Produto Sem Descrição",
        "codigo_barra": "7891234567891"
    }
    response = client.post("/produtos", json=produto_sem_descricao)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["descricao"] == ""


# ── Novos testes (GET, PUT, DELETE) ──────────────────────────────


def test_listar_produtos_vazio(client):
    """Testa listagem quando não há produtos"""
    response = client.get("/produtos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_listar_produtos(client, produto_criado):
    """Testa listagem de produtos"""
    response = client.get("/produtos")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["id"] == produto_criado["id"]


def test_listar_produtos_busca(client, produto_criado):
    """Testa busca de produtos por nome"""
    nome = produto_criado["nome"]
    response = client.get(f"/produtos?busca={nome[:5]}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert any(p["id"] == produto_criado["id"] for p in data)


def test_listar_produtos_busca_sem_resultado(client, produto_criado):
    """Testa busca que não retorna resultados"""
    response = client.get("/produtos?busca=xyzxyzxyz999")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_atualizar_produto(client, produto_criado):
    """Testa atualização de produto"""
    produto_id = produto_criado["id"]
    response = client.put(f"/produtos/{produto_id}", json={"nome": "Nome Atualizado"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["nome"] == "Nome Atualizado"


def test_atualizar_produto_inexistente(client):
    """Testa atualização de produto que não existe"""
    response = client.put("/produtos/99999", json={"nome": "Qualquer"})
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_deletar_produto_sem_recebimentos(client, produto_criado):
    """Testa exclusão de produto sem recebimentos"""
    produto_id = produto_criado["id"]
    response = client.delete(f"/produtos/{produto_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Confirma que foi removido da listagem
    lista = client.get("/produtos").json()
    assert not any(p["id"] == produto_id for p in lista)


def test_deletar_produto_com_recebimentos(client, produto_criado, sessao_criada):
    """Testa que produto com recebimentos não pode ser excluído"""
    sessao_id = sessao_criada["id"]
    codigo_barra = produto_criado["codigo_barra"]

    # Registra recebimento
    client.post(
        f"/recebimentos/salvar/{sessao_id}",
        json={"codigo_barra": codigo_barra, "quantidade": 2}
    )

    response = client.delete(f"/produtos/{produto_criado['id']}")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "recebimento" in response.json()["detail"].lower()


def test_deletar_produto_inexistente(client):
    """Testa exclusão de produto que não existe"""
    response = client.delete("/produtos/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
