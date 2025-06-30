from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from venda.model import ModeloVenda
from cliente.model import ModeloCliente
from produto.model import ModeloProduto
from database import get_db
from venda.schemas import VendaCreate, VendaBase

router = APIRouter()

@router.get("/vendas", response_model=list[VendaBase])
def listar_vendas(db: Session = Depends(get_db)):
    return db.query(ModeloVenda).all()

@router.post("/vendas", response_model=VendaBase)
def adicionar_venda(venda: VendaCreate, db: Session = Depends(get_db)):
    cliente = db.query(ModeloCliente).filter(ModeloCliente.id == venda.cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    produto = db.query(ModeloProduto).filter(ModeloProduto.id == venda.produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    nova_venda = ModeloVenda(
        cliente_id=venda.cliente_id,
        produto_id=venda.produto_id,
        quantidade=venda.quantidade,
        valor_total=0.00
    )
    
    db.add(nova_venda)
    db.commit()
    nova_venda.valor_total = nova_venda.quantidade * produto.valor 
    db.commit()
    db.refresh(nova_venda)
    
    return nova_venda


@router.get("/vendas/{venda_id}", response_model=VendaBase)
def buscar_venda(venda_id: int, db: Session = Depends(get_db)):
    venda = db.query(ModeloVenda).filter(ModeloVenda.id == venda_id).first()
    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return venda

@router.delete("/vendas/{venda_id}")
def remover_venda(venda_id: int, db: Session = Depends(get_db)):
    venda = db.query(ModeloVenda).filter(ModeloVenda.id == venda_id).first()
    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    db.delete(venda)
    db.commit()
    return {"message": "Venda removida com sucesso!"}