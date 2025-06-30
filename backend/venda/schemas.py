from pydantic import BaseModel
from typing import Optional

class VendaBase(BaseModel):
    id: Optional[int] = None
    cliente_id: int
    produto_id: int
    quantidade: int
    valor_total: Optional[float] = None

    class Config:
        orm_mode = True

class VendaCreate(BaseModel):
    cliente_id: int
    produto_id: int
    quantidade: int

    class Config:
        orm_mode = True
