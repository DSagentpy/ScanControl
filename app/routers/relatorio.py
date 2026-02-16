from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi.responses import FileResponse
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
from app.database import get_db
from app import models
import uuid

router = APIRouter()


def get_ultima_sessao(db: Session):
    return db.query(models.Sessao).order_by(
        models.Sessao.id.desc()
    ).first()


@router.get("/relatorio/pdf")
def gerar_pdf(
    titulo: str = Query("Relatório de Conferência"),
    db: Session = Depends(get_db)
):

    sessao = get_ultima_sessao(db)

    if not sessao:
        raise HTTPException(status_code=404, detail="Nenhuma sessão encontrada")

    resultados = db.query(
        models.Produto.codigo,
        models.Produto.descricao,
        models.Produto.codigo_barra,
        func.sum(models.Recebimento.quantidade).label("total")
    ).join(
        models.Recebimento,
        models.Produto.id == models.Recebimento.produto_id
    ).filter(
        models.Recebimento.sessao_id == sessao.id
    ).group_by(
        models.Produto.codigo,
        models.Produto.descricao,
        models.Produto.codigo_barra
    ).all()

    if not resultados:
        raise HTTPException(status_code=400, detail="Nenhum produto na sessão")

    file_path = f"relatorio_{uuid.uuid4().hex}.pdf"
    doc = SimpleDocTemplate(file_path)

    elements = []
    styles = getSampleStyleSheet()

    # 🔥 TÍTULO
    elements.append(Paragraph(f"<b>{titulo}</b>", styles["Title"]))
    elements.append(Spacer(1, 20))

    # 🔥 INFORMAÇÕES DA SESSÃO
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
    elements.append(Paragraph(f"Sessão Nº: {sessao.id}", styles["Normal"]))
    elements.append(Paragraph(f"Data: {data_atual}", styles["Normal"]))
    elements.append(Spacer(1, 20))

    # 🔥 TABELA
    data = [["Código", "Descrição", "Código de Barra", "Quantidade"]]

    total_geral = 0

    for r in resultados:
        total_geral += r.total
        data.append([r.codigo, r.descricao, r.codigo_barra, str(r.total)])

    # Linha de total
    data.append(["", "", "TOTAL GERAL", str(total_geral)])

    table = Table(data, repeatRows=1)

    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('BACKGROUND', (-2, -1), (-1, -1), colors.lightgrey),
        ('SPAN', (0, -1), (1, -1)),
    ]))

    elements.append(table)

    doc.build(elements)

    return FileResponse(file_path, filename="relatorio.pdf")
