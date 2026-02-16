from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

router = APIRouter()

@router.post("/sessao/nova", status_code=status.HTTP_200_OK)
def nova_sessao(db: Session = Depends(get_db)):

    # Apaga todos os recebimentos
    db.query(models.Recebimento).delete()
    db.commit()

    # Cria nova sessão
    sessao = models.Sessao()
    db.add(sessao)
    db.commit()
    db.refresh(sessao)

    return {
        "id": sessao.id,
        "status": "conferência reiniciada"
    }
