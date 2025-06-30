from sqlalchemy.orm import Session
from fastapi import HTTPException
from pagamento.model import ModeloPagamento
from pagamento.schemas import PagamentoCreate

class ControlePagamento:
    def __init__(self, db: Session):
        self.db = db

    def listar_pagamentos(self):
        return self.db.query(ModeloPagamento).all()

    def adicionar_pagamento(self, pagamento_data: PagamentoCreate):
        novo_pagamento = ModeloPagamento(**pagamento_data.dict())
        self.db.add(novo_pagamento)
        self.db.commit()
        self.db.refresh(novo_pagamento)
        return novo_pagamento

    def buscar_pagamento_por_id(self, pagamento_id: int):
        pagamento = self.db.query(ModeloPagamento).filter(ModeloPagamento.id == pagamento_id).first()
        if not pagamento:
            raise HTTPException(status_code=404, detail="Pagamento não encontrado")
        return pagamento

    def atualizar_pagamento(self, pagamento_id: int, novos_dados: dict):
        pagamento = self.buscar_pagamento_por_id(pagamento_id)
        for chave, valor in novos_dados.items():
            setattr(pagamento, chave, valor)
        self.db.commit()
        self.db.refresh(pagamento)
        return pagamento

    def deletar_pagamento(self, pagamento_id: int):
        pagamento = self.buscar_pagamento_por_id(pagamento_id)
        self.db.delete(pagamento)
        self.db.commit()
        return {"detail": "Pagamento removido com sucesso!"}
