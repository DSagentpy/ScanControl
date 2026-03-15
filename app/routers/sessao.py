from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter()


# Criar nova sessão (nome opcional)
@router.post("/sessao")
def criar_sessao(
    dados: Optional[schemas.SessaoCreate] = Body(default=None),
    db: Session = Depends(get_db)
):
    nome = dados.nome if dados and dados.nome else None
    sessao = models.Sessao(nome=nome)
    db.add(sessao)
    db.commit()
    db.refresh(sessao)
    return {
        "id": sessao.id,
        "nome": sessao.nome,
        "criada_em": sessao.criada_em.isoformat() if sessao.criada_em else None
    }


# Listar todas as sessões
@router.get("/sessao")
def listar_sessoes(db: Session = Depends(get_db)):
    sessoes = db.query(models.Sessao).order_by(models.Sessao.id.desc()).all()
    return [
        {
            "id": s.id,
            "nome": s.nome,
            "criada_em": s.criada_em.isoformat() if s.criada_em else None
        }
        for s in sessoes
    ]


# Renomear sessão
@router.patch("/sessao/{sessao_id}")
def renomear_sessao(
    sessao_id: int,
    dados: schemas.SessaoCreate,
    db: Session = Depends(get_db)
):
    sessao = db.query(models.Sessao).filter(
        models.Sessao.id == sessao_id
    ).first()

    if not sessao:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")

    sessao.nome = dados.nome or None
    db.commit()
    db.refresh(sessao)

    return {
        "id": sessao.id,
        "nome": sessao.nome,
        "criada_em": sessao.criada_em.isoformat() if sessao.criada_em else None
    }


# Excluir sessão e seus recebimentos
@router.delete("/sessao/{sessao_id}")
def excluir_sessao(sessao_id: int, db: Session = Depends(get_db)):
    sessao = db.query(models.Sessao).filter(
        models.Sessao.id == sessao_id
    ).first()

    if not sessao:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")

    db.query(models.Recebimento).filter(
        models.Recebimento.sessao_id == sessao_id
    ).delete()

    db.delete(sessao)
    db.commit()

    return {"message": "Sessão excluída"}
