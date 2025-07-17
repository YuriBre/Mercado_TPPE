from pydantic import BaseModel
from typing import Optional
from datetime import date
from cliente.schemas import ClienteResponse
from produto.schemas import ProdutoResponse
from vendedor.schemas import VendedorResponse

class VendaBase(BaseModel):
    id: Optional[int] = None
    cliente_cpf: str
    vendedor_cpf: str
    produto_id: int
    quantidade: int
    valor_total: Optional[float] = None

    class Config:
        orm_mode = True

class VendaCreate(BaseModel):
    cliente_cpf: str
    vendedor_cpf: str
    produto_id: int
    quantidade: int

    class Config:
        orm_mode = True


class VendaResponse(BaseModel):
    id: int
    data: date
    quantidade: int
    total: float
    comissao: float
    cliente: ClienteResponse
    produto: ProdutoResponse
    vendedor: VendedorResponse

    class Config:
        orm_mode = True