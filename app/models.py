from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, func
from sqlalchemy.orm import relationship
from app.database import Base


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, index=True)
    nome = Column(String, index=True)
    codigo_barra = Column(String, unique=True, index=True)
    descricao = Column(String, default="")


class Sessao(Base):
    __tablename__ = "sessao"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=True)
    criada_em = Column(DateTime, default=func.now(), server_default=func.now())


class Recebimento(Base):
    __tablename__ = "recebimentos"

    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    sessao_id = Column(Integer, ForeignKey("sessao.id"), index=True)
    quantidade = Column(Integer)
    escaneado_em = Column(DateTime, default=func.now(), server_default=func.now())

    produto = relationship("Produto")


# ── Auditoria de Inventário ───────────────────────────────────────────────────

class ConciliacaoAuditoria(Base):
    """Cabeçalho de uma auditoria: une sessão de scanner com arquivo do ERP."""
    __tablename__ = "conciliacao_auditoria"

    id = Column(Integer, primary_key=True, index=True)
    sessao_id = Column(Integer, ForeignKey("sessao.id"), index=True)
    nome = Column(String, nullable=True)
    criada_em = Column(DateTime, default=func.now(), server_default=func.now())
    acuracidade_geral = Column(Float, nullable=True)
    total_itens_fisico = Column(Integer, nullable=True)
    total_itens_sistemico = Column(Integer, nullable=True)

    itens = relationship(
        "ItemConciliacao",
        back_populates="auditoria",
        cascade="all, delete-orphan"
    )


class ItemConciliacao(Base):
    """Linha de resultado da conciliação por produto."""
    __tablename__ = "item_conciliacao"

    id = Column(Integer, primary_key=True, index=True)
    auditoria_id = Column(Integer, ForeignKey("conciliacao_auditoria.id"), index=True)
    codigo_barra = Column(String, index=True)
    nome_produto = Column(String)
    qtd_fisica = Column(Integer, default=0)       # escaneado
    qtd_sistemica = Column(Integer, default=0)    # ERP
    estoque_minimo = Column(Integer, default=0)
    divergencia = Column(Integer)                 # fisica - sistemica
    acuracidade_item = Column(Float)              # %
    # OK | DIVERGENTE | CRITICO | FANTASMA | NAO_SISTEMICO | RUPTURA
    status = Column(String)

    auditoria = relationship("ConciliacaoAuditoria", back_populates="itens")
