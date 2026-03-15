import os
import logging
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from pathlib import Path
from sqlalchemy import text

from app.database import Base, engine
from app.routers import produtos, recebimentos, sessao, relatorio, conciliacao

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Sistema de Auditoria Logística")


def run_migrations():
    """Adiciona colunas novas em tabelas existentes sem apagar dados."""
    stmts = [
        "ALTER TABLE sessao ADD COLUMN nome VARCHAR",
        "ALTER TABLE recebimentos ADD COLUMN escaneado_em DATETIME DEFAULT CURRENT_TIMESTAMP",
    ]
    with engine.connect() as conn:
        for sql in stmts:
            try:
                conn.execute(text(sql))
                conn.commit()
            except Exception:
                pass  # coluna já existe


logger.info("Criando/verificando tabelas...")
Base.metadata.create_all(bind=engine)
run_migrations()

# Routers
app.include_router(produtos.router)
app.include_router(recebimentos.router)
app.include_router(sessao.router)
app.include_router(relatorio.router)
app.include_router(conciliacao.router)


# ── Exception handlers ────────────────────────────────────────────────────────

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Erro de validação: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Erro não tratado: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno do servidor"}
    )


# ── Páginas HTML ──────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
def home():
    caminho = Path(__file__).parent / "templates" / "coletor.html"
    return caminho.read_text(encoding="utf-8")


@app.get("/auditoria", response_class=HTMLResponse)
def auditoria():
    caminho = Path(__file__).parent / "templates" / "auditoria.html"
    return caminho.read_text(encoding="utf-8")
