from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi.responses import StreamingResponse

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    HRFlowable,
    PageTemplate,
    Frame
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from datetime import datetime
from io import BytesIO

from app.database import get_db
from app import models

router = APIRouter()


# 🔹 Busca última sessão
def get_ultima_sessao(db: Session):
    return db.query(models.Sessao).order_by(
        models.Sessao.id.desc()
    ).first()


# 🔹 Header e Footer estilo ERP
def header_footer(canvas_obj, doc):
    canvas_obj.saveState()
    width, height = A4

    # Cabeçalho
    canvas_obj.setFont("Helvetica-Bold", 10)
    canvas_obj.drawString(2 * cm, height - 1.5 * cm,
                          "SISTEMA DE CONTROLE LOGÍSTICO")

    canvas_obj.setFont("Helvetica", 8)
    canvas_obj.drawRightString(
        width - 2 * cm,
        height - 1.5 * cm,
        f"Emitido em: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    )

    # Rodapé
    canvas_obj.setFont("Helvetica", 8)
    canvas_obj.drawCentredString(width / 2, 1.2 * cm,
                                 f"Página {doc.page}")

    canvas_obj.restoreState()


# 🔥 Endpoint PDF
@router.get("/relatorio/pdf")
def gerar_pdf(
    titulo: str = Query("Relatório de Conferência"),
    db: Session = Depends(get_db)
):

    sessao = get_ultima_sessao(db)

    if not sessao:
        raise HTTPException(status_code=404,
                            detail="Nenhuma sessão encontrada")

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
        raise HTTPException(status_code=400,
                            detail="Nenhum produto na sessão")

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=3 * cm,
        bottomMargin=2 * cm
    )

    elements = []
    styles = getSampleStyleSheet()

    # 🔹 Título
    titulo_style = ParagraphStyle(
        'TituloERP',
        parent=styles['Title'],
        fontSize=16,
        textColor=colors.HexColor("#1F4E79")
    )

    elements.append(Paragraph(titulo, titulo_style))
    elements.append(Spacer(1, 12))
    elements.append(HRFlowable(width="100%", thickness=1,
                               color=colors.grey))
    elements.append(Spacer(1, 20))

    # 🔹 Informações da sessão
    elements.append(Paragraph(
        f"<b>Número da Sessão:</b> {sessao.id}",
        styles["Normal"]
    ))
    elements.append(Spacer(1, 12))

    # 🔹 Tabela
    data = [["Código", "Descrição",
             "Código de Barra", "Quantidade"]]

    total_geral = 0
    total_itens = len(resultados)

    for r in resultados:
        total_geral += r.total
        data.append([
            r.codigo,
            r.descricao,
            r.codigo_barra,
            str(r.total)
        ])

    table = Table(
        data,
        colWidths=[3 * cm, 6 * cm, 4 * cm, 3 * cm],
        repeatRows=1
    )

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0),
         colors.HexColor("#D9D9D9")),
        ('FONTNAME', (0, 0), (-1, 0),
         'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('GRID', (0, 0), (-1, -1),
         0.3, colors.grey),
        ('ALIGN', (-1, 1), (-1, -1),
         'CENTER'),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 25))

    # 🔹 Resumo executivo
    resumo_data = [
        ["Total de Produtos Diferentes:",
         str(total_itens)],
        ["Quantidade Total Recebida:",
         str(total_geral)]
    ]

    resumo_table = Table(resumo_data,
                         colWidths=[8 * cm, 3 * cm])

    resumo_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1),
         colors.HexColor("#F2F2F2")),
        ('GRID', (0, 0), (-1, -1),
         0.5, colors.grey),
        ('FONTNAME', (0, 0), (-1, -1),
         'Helvetica-Bold'),
        ('ALIGN', (-1, 0), (-1, -1),
         'CENTER')
    ]))

    elements.append(resumo_table)

    # 🔹 Template com header/footer
    frame = Frame(
        doc.leftMargin,
        doc.bottomMargin,
        doc.width,
        doc.height,
        id='normal'
    )

    template = PageTemplate(
        id='ERPTemplate',
        frames=frame,
        onPage=header_footer
    )

    doc.addPageTemplates([template])
    doc.build(elements)

    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition":
            "attachment; filename=relatorio_erp.pdf"
        }
    )
