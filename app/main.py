import os
import logging
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from pathlib import Path
from sqlalchemy import text

from app.database import Base, engine, SessionLocal
from app.routers import produtos, recebimentos, sessao, relatorio

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Scanner Logístico Profissional")


def run_migrations():
    """Adiciona colunas novas em tabelas existentes sem apagar dados."""
    novas_colunas = [
        ("sessao",       "ALTER TABLE sessao ADD COLUMN nome VARCHAR"),
        ("recebimentos", "ALTER TABLE recebimentos ADD COLUMN escaneado_em DATETIME DEFAULT CURRENT_TIMESTAMP"),
    ]
    with engine.connect() as conn:
        for tabela, sql in novas_colunas:
            try:
                conn.execute(text(sql))
                conn.commit()
                logger.info(f"Migração aplicada: {tabela}")
            except Exception:
                pass  # Coluna já existe


# Cria tabelas e roda migrações
logger.info("Criando tabelas do banco de dados...")
Base.metadata.create_all(bind=engine)
run_migrations()

app.include_router(produtos.router)
app.include_router(recebimentos.router)
app.include_router(sessao.router)
app.include_router(relatorio.router)


# Tratamento global de erros de validação
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Erro de validação: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body}
    )


# Tratamento global de erros genéricos
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Erro não tratado: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno do servidor"}
    )


@app.get("/", response_class=HTMLResponse)
def home():
    caminho = Path(__file__).parent / "templates" / "coletor.html"
    return caminho.read_text(encoding="utf-8")
