from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String)  # 🔥 ADICIONE ISSO
    nome = Column(String)
    codigo_barra = Column(String, unique=True)
    descricao = Column(String)


class Sessao(Base):
    __tablename__ = "sessao"

    id = Column(Integer, primary_key=True, index=True)

class Recebimento(Base):
    __tablename__ = "recebimentos"

    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    sessao_id = Column(Integer, ForeignKey("sessao.id"))
    quantidade = Column(Integer)

    produto = relationship("Produto")