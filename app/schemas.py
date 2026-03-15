from typing import Optional
from pydantic import BaseModel, Field, field_validator


class ProdutoCreate(BaseModel):
    codigo: str = Field(..., min_length=1, description="Código interno do produto")
    nome: str = Field(..., min_length=1, description="Nome do produto")
    codigo_barra: str = Field(..., min_length=1, description="Código de barras único")
    descricao: str = Field(default="", description="Descrição do produto")

    @field_validator("codigo", "nome", "codigo_barra")
    @classmethod
    def validar_campos_obrigatorios(cls, v):
        if not v or not v.strip():
            raise ValueError("Campo não pode estar vazio")
        return v.strip()


class ProdutoUpdate(BaseModel):
    codigo: Optional[str] = Field(default=None)
    nome: Optional[str] = Field(default=None)
    descricao: Optional[str] = Field(default=None)

    @field_validator("codigo", "nome")
    @classmethod
    def validar_se_fornecido(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Campo não pode estar vazio")
        return v.strip() if v else v


class SessaoCreate(BaseModel):
    nome: Optional[str] = Field(default=None, description="Nome opcional para identificar a sessão")


class RecebimentoCreate(BaseModel):
    codigo_barra: str = Field(..., min_length=1, description="Código de barras do produto")
    quantidade: int = Field(..., gt=0, description="Quantidade recebida (deve ser maior que zero)")

    @field_validator("codigo_barra")
    @classmethod
    def validar_codigo_barra(cls, v):
        if not v or not v.strip():
            raise ValueError("Código de barras não pode estar vazio")
        return v.strip()


class CodigoBarra(BaseModel):
    codigo_barra: str = Field(..., min_length=1, description="Código de barras para verificação")

    @field_validator("codigo_barra")
    @classmethod
    def validar_codigo_barra(cls, v):
        if not v or not v.strip():
            raise ValueError("Código de barras não pode estar vazio")
        return v.strip()
