from pydantic import BaseModel


class ProdutoCreate(BaseModel):
    codigo: str
    nome: str
    codigo_barra: str
    descricao: str


class RecebimentoCreate(BaseModel):
    codigo_barra: str
    quantidade: int
class CodigoBarra(BaseModel):
    codigo_barra: str

