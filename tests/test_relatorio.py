"""
Testes para o router de relatório
"""
import pytest
from fastapi import status


def test_gerar_pdf_sem_sessao(client):
    """Testa geração de PDF sem sessões"""
    response = client.get("/relatorio/pdf")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "nenhuma sessão" in response.json()["detail"].lower()


def test_gerar_pdf_sessao_vazia(client, sessao_criada):
    """Testa geração de PDF com sessão vazia"""
    response = client.get("/relatorio/pdf")
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "nenhum produto" in response.json()["detail"].lower()


def test_gerar_pdf_sucesso(client, produto_criado, sessao_criada):
    """Testa geração de PDF com sucesso"""
    sessao_id = sessao_criada["id"]
    codigo_barra = produto_criado["codigo_barra"]
    
    # Adiciona recebimento
    client.post(
        f"/recebimentos/salvar/{sessao_id}",
        json={"codigo_barra": codigo_barra, "quantidade": 5}
    )
    
    # Gera PDF
    response = client.get("/relatorio/pdf")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "application/pdf"
    assert "attachment" in response.headers["content-disposition"]
    assert len(response.content) > 0


def test_gerar_pdf_com_sessao_id(client, produto_criado, sessao_criada):
    """Testa geração de PDF especificando sessão_id"""
    sessao_id = sessao_criada["id"]
    codigo_barra = produto_criado["codigo_barra"]
    
    # Adiciona recebimento
    client.post(
        f"/recebimentos/salvar/{sessao_id}",
        json={"codigo_barra": codigo_barra, "quantidade": 3}
    )
    
    # Gera PDF com sessao_id
    response = client.get(f"/relatorio/pdf?sessao_id={sessao_id}")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "application/pdf"


def test_gerar_pdf_com_titulo_customizado(client, produto_criado, sessao_criada):
    """Testa geração de PDF com título customizado"""
    sessao_id = sessao_criada["id"]
    codigo_barra = produto_criado["codigo_barra"]
    
    # Adiciona recebimento
    client.post(
        f"/recebimentos/salvar/{sessao_id}",
        json={"codigo_barra": codigo_barra, "quantidade": 2}
    )
    
    # Gera PDF com título customizado
    response = client.get("/relatorio/pdf?titulo=Relatório%20Customizado")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "application/pdf"


def test_gerar_pdf_multiplos_produtos(client, sessao_criada):
    """Testa geração de PDF com múltiplos produtos"""
    sessao_id = sessao_criada["id"]
    
    # Cria múltiplos produtos
    produto1 = client.post("/produtos", json={
        "codigo": "PROD001",
        "nome": "Produto 1",
        "codigo_barra": "7891234567890",
        "descricao": "Descrição 1"
    }).json()
    
    produto2 = client.post("/produtos", json={
        "codigo": "PROD002",
        "nome": "Produto 2",
        "codigo_barra": "7891234567891",
        "descricao": "Descrição 2"
    }).json()
    
    # Adiciona recebimentos
    client.post(
        f"/recebimentos/salvar/{sessao_id}",
        json={"codigo_barra": produto1["codigo_barra"], "quantidade": 5}
    )
    client.post(
        f"/recebimentos/salvar/{sessao_id}",
        json={"codigo_barra": produto2["codigo_barra"], "quantidade": 10}
    )
    
    # Gera PDF
    response = client.get("/relatorio/pdf")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "application/pdf"
    # Verifica que o PDF contém dados (tamanho razoável)
    assert len(response.content) > 1000

