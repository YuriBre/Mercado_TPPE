import enum
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MetodoPagamentoEnum(str, enum.Enum):
    dinheiro = "dinheiro"
    cartao = "cartao"
    pix = "pix"
    boleto = "boleto"

class PagamentoBase(BaseModel):
    id: Optional[int] = None
    venda_id: int
    valor_pago: float
    metodo_pagamento: MetodoPagamentoEnum
    data_pagamento: Optional[datetime] = None

    class Config:
        orm_mode = True

class PagamentoCreate(BaseModel):
    venda_id: int
    valor_pago: float
    metodo_pagamento: MetodoPagamentoEnum
