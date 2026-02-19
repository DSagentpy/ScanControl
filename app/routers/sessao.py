from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

router = APIRouter()

# Criar nova sessão
@router.post("/sessao")
def criar_sessao(db: Session = Depends(get_db)):
    sessao = models.Sessao()
    db.add(sessao)
    db.commit()
    db.refresh(sessao)
    return sessao


# Listar todas as sessões
@router.get("/sessao")
def listar_sessoes(db: Session = Depends(get_db)):
    return db.query(models.Sessao).order_by(
        models.Sessao.id.desc()
    ).all()


# Excluir sessão
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
