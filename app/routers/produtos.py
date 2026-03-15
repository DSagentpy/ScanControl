from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter()


# Listar produtos com busca opcional
@router.get("/produtos")
def listar_produtos(
    busca: str = Query(default="", description="Filtrar por nome, código ou código de barras"),
    db: Session = Depends(get_db)
):
    query = db.query(models.Produto)
    if busca.strip():
        termo = f"%{busca.strip()}%"
        query = query.filter(
            models.Produto.nome.ilike(termo) |
            models.Produto.codigo.ilike(termo) |
            models.Produto.codigo_barra.ilike(termo)
        )
    return query.order_by(models.Produto.nome).all()


# Criar produto
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

    produto = models.Produto(**dados.model_dump())
    db.add(produto)
    db.commit()
    db.refresh(produto)

    return {
        "id": produto.id,
        "codigo": produto.codigo,
        "nome": produto.nome,
        "codigo_barra": produto.codigo_barra,
        "descricao": produto.descricao
    }


# Atualizar produto
@router.put("/produtos/{produto_id}")
def atualizar_produto(
    produto_id: int,
    dados: schemas.ProdutoUpdate,
    db: Session = Depends(get_db)
):
    produto = db.query(models.Produto).filter(
        models.Produto.id == produto_id
    ).first()

    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    for campo, valor in dados.model_dump(exclude_none=True).items():
        setattr(produto, campo, valor)

    db.commit()
    db.refresh(produto)

    return {
        "id": produto.id,
        "codigo": produto.codigo,
        "nome": produto.nome,
        "codigo_barra": produto.codigo_barra,
        "descricao": produto.descricao
    }


# Excluir produto (apenas se não tiver recebimentos)
@router.delete("/produtos/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(models.Produto).filter(
        models.Produto.id == produto_id
    ).first()

    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    total_recebimentos = db.query(models.Recebimento).filter(
        models.Recebimento.produto_id == produto_id
    ).count()

    if total_recebimentos > 0:
        raise HTTPException(
            status_code=400,
            detail=f"Produto possui {total_recebimentos} recebimento(s) registrado(s) e não pode ser excluído"
        )

    db.delete(produto)
    db.commit()
