"""
Testes para o main.py
"""
import pytest
from fastapi import status


def test_home_endpoint(client):
    """Testa endpoint raiz retorna HTML"""
    response = client.get("/")
    
    assert response.status_code == status.HTTP_200_OK
    assert "text/html" in response.headers["content-type"]
    assert "Scanner Logístico" in response.text


def test_erro_validacao(client):
    """Testa tratamento de erro de validação"""
    # Tenta criar produto com dados inválidos
    response = client.post("/produtos", json={
        "codigo": "",
        "nome": "",
        "codigo_barra": "",
        "quantidade": -1  # Campo que não existe
    })
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in response.json()

