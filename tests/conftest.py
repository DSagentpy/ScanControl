"""
Configuração de fixtures para testes
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.database import Base, get_db
from app.main import app


# Banco de dados de teste em memória
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Cria uma sessão de banco de dados para cada teste"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Cria um cliente de teste FastAPI"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def produto_exemplo():
    """Dados de exemplo para produto"""
    return {
        "codigo": "PROD001",
        "nome": "Produto Teste",
        "codigo_barra": "7891234567890",
        "descricao": "Descrição do produto teste"
    }


@pytest.fixture
def produto_criado(client, produto_exemplo):
    """Cria um produto no banco de teste"""
    response = client.post("/produtos", json=produto_exemplo)
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def sessao_criada(client):
    """Cria uma sessão no banco de teste"""
    response = client.post("/sessao")
    assert response.status_code == 200
    return response.json()

