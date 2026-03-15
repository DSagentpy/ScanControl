"""
Testes para o router de sessão
"""
import pytest
from fastapi import status


def test_criar_sessao_sem_body(client):
    """Testa criação de sessão sem body (retrocompatível)"""
    response = client.post("/sessao")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "id" in data
    assert "criada_em" in data


def test_criar_sessao_com_nome(client):
    """Testa criação de sessão com nome"""
    response = client.post("/sessao", json={"nome": "Conferência Manhã"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["nome"] == "Conferência Manhã"
    assert "id" in data


def test_criar_sessao_nome_vazio(client):
    """Testa que nome vazio é aceito (campo opcional)"""
    response = client.post("/sessao", json={"nome": ""})
    assert response.status_code == status.HTTP_200_OK


def test_renomear_sessao(client, sessao_criada):
    """Testa renomear sessão"""
    sessao_id = sessao_criada["id"]
    response = client.patch(f"/sessao/{sessao_id}", json={"nome": "Novo Nome"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["nome"] == "Novo Nome"


def test_renomear_sessao_inexistente(client):
    """Testa renomear sessão que não existe"""
    response = client.patch("/sessao/99999", json={"nome": "X"})
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_listar_sessoes(client, sessao_criada):
    """Testa listagem de sessões"""
    response = client.get("/sessao")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["id"] == sessao_criada["id"]


def test_listar_sessoes_ordenadas(client):
    """Testa que sessões são listadas em ordem decrescente"""
    # Cria múltiplas sessões
    sessao1 = client.post("/sessao").json()
    sessao2 = client.post("/sessao").json()
    sessao3 = client.post("/sessao").json()
    
    response = client.get("/sessao")
    assert response.status_code == status.HTTP_200_OK
    sessoes = response.json()
    
    # Verifica que estão em ordem decrescente
    ids = [s["id"] for s in sessoes]
    assert ids == sorted(ids, reverse=True)


def test_excluir_sessao(client, sessao_criada):
    """Testa exclusão de sessão"""
    sessao_id = sessao_criada["id"]
    
    response = client.delete(f"/sessao/{sessao_id}")
    
    assert response.status_code == status.HTTP_200_OK
    assert "message" in response.json()
    
    # Verifica que a sessão foi excluída
    response_get = client.get("/sessao")
    sessoes = response_get.json()
    sessao_ids = [s["id"] for s in sessoes]
    assert sessao_id not in sessao_ids


def test_excluir_sessao_inexistente(client):
    """Testa exclusão de sessão que não existe"""
    response = client.delete("/sessao/99999")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "não encontrada" in response.json()["detail"].lower()

