from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pagamento.control import ControlePagamento
from pagamento.schemas import PagamentoCreate, PagamentoBase
from database import get_db

router = APIRouter()

@router.get("/pagamentos", response_model=list[PagamentoBase])
def listar_pagamentos(db: Session = Depends(get_db)):
    controle = ControlePagamento(db)
    return controle.listar_pagamentos()

@router.post("/pagamentos", response_model=PagamentoBase)
def adicionar_pagamento(pagamento: PagamentoCreate, db: Session = Depends(get_db)):
    controle = ControlePagamento(db)
    return controle.adicionar_pagamento(pagamento)

@router.get("/pagamentos/{id}", response_model=PagamentoBase)
def buscar_pagamento(id: int, db: Session = Depends(get_db)):
    controle = ControlePagamento(db)
    return controle.buscar_pagamento_por_id(id)

@router.put("/pagamentos/{id}", response_model=PagamentoBase)
def atualizar_pagamento(id: int, pagamento_update: PagamentoCreate, db: Session = Depends(get_db)):
    controle = ControlePagamento(db)
    novos_dados = pagamento_update.dict(exclude_unset=True)
    return controle.atualizar_pagamento(id, novos_dados)

@router.delete("/pagamentos/{id}")
def deletar_pagamento(id: int, db: Session = Depends(get_db)):
    controle = ControlePagamento(db)
    return controle.deletar_pagamento(id)
