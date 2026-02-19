from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app import models, schemas
from app.schemas import CodigoBarra


router = APIRouter()


def get_produto_por_codigo(db: Session, codigo: str):
    return db.query(models.Produto).filter(
        models.Produto.codigo_barra == codigo
    ).first()


def get_ultima_sessao(db: Session):

    sessao = db.query(models.Sessao).order_by(
        models.Sessao.id.desc()
    ).first()

    if not sessao:
        sessao = models.Sessao()
        db.add(sessao)
        db.commit()
        db.refresh(sessao)

    return sessao



@router.post("/recebimentos/verificar")
def verificar(dados: CodigoBarra, db: Session = Depends(get_db)):

    produto = db.query(models.Produto).filter(
        models.Produto.codigo_barra == dados.codigo_barra
    ).first()

    if produto:
        return {
            "cadastrado": True,
            "nome": produto.nome
        }
    else:
        return {
            "cadastrado": False
        }



@router.post("/recebimentos/salvar/{sessao_id}")
def salvar_recebimento(
    sessao_id: int,
    dados: schemas.RecebimentoCreate,
    db: Session = Depends(get_db)
):

    produto = db.query(models.Produto).filter(
        models.Produto.codigo_barra == dados.codigo_barra
    ).first()

    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    novo = models.Recebimento(
        produto_id=produto.id,
        quantidade=dados.quantidade,
        sessao_id=sessao_id
    )

    db.add(novo)
    db.commit()

    total_produto = db.query(func.sum(models.Recebimento.quantidade)).filter(
        models.Recebimento.produto_id == produto.id,
        models.Recebimento.sessao_id == sessao_id
    ).scalar()

    return {"quantidade_total": total_produto or 0}



@router.get("/recebimentos/lista/{sessao_id}")
def lista_produtos_sessao(sessao_id: int, db: Session = Depends(get_db)):

    resultados = db.query(
        models.Produto.nome,
        func.sum(models.Recebimento.quantidade).label("total")
    ).join(
        models.Recebimento,
        models.Produto.id == models.Recebimento.produto_id
    ).filter(
        models.Recebimento.sessao_id == sessao_id
    ).group_by(
        models.Produto.nome
    ).order_by(
        func.sum(models.Recebimento.quantidade).desc()
    ).all()

    return [{"nome": r.nome, "total": r.total} for r in resultados]
