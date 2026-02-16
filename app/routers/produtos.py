from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter()

@router.post("/produtos", status_code=status.HTTP_201_CREATED)
def criar_produto(dados: schemas.ProdutoCreate, db: Session = Depends(get_db)):

    produto_existente = db.query(models.Produto).filter(
        models.Produto.codigo_barra == dados.codigo_barra
    ).first()

    if produto_existente:
        raise HTTPException(
            status_code=400,
            detail="Produto já cadastrado"
        )

    produto = models.Produto(**dados.dict())

    db.add(produto)
    db.commit()
    db.refresh(produto)

    return {
        "id": produto.id,
        "nome": produto.nome,
        "codigo_barra": produto.codigo_barra,
        "descricao": produto.descricao
    }
