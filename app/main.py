from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pathlib import Path
from app.database import Base, engine
from app.routers import produtos, recebimentos, sessao, relatorio

app = FastAPI(title="Scanner Logístico Profissional")

Base.metadata.create_all(bind=engine)

app.include_router(produtos.router)
app.include_router(recebimentos.router)
app.include_router(sessao.router)
app.include_router(relatorio.router)

@app.get("/", response_class=HTMLResponse)
def home():
    caminho = Path(__file__).parent / "templates" / "coletor.html"
    return caminho.read_text(encoding="utf-8")
