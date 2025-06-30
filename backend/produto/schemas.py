from pydantic import BaseModel
from typing import Optional
    
class ProdutoBase(BaseModel):
    id: Optional[int] = None
    nome: str
    descricao: str
    valor: float
    lucro_percentual: float
    qtd_estoque: int

    class Config:
        orm_mode = True

class ProdutoCreate(BaseModel):
    nome: str
    descricao: str
    valor: float
    lucro_percentual: float
    qtd_estoque: int
