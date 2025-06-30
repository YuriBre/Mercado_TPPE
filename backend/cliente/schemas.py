from pydantic import BaseModel
from typing import Optional

class ClienteBase(BaseModel):
    id: Optional[int] = None
    nome: str
    endereco: Optional[str] = None
    telefone: Optional[str] = None

    class Config:
        orm_mode = True

class ClienteCreate(ClienteBase):
    endereco: Optional[str] = None
    telefone: Optional[str] = None
