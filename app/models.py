from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
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
