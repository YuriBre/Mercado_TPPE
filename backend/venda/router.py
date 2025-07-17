from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from venda.model import ModeloVenda
from cliente.model import ModeloCliente
from produto.model import ModeloProduto
from database import get_db
from venda.schemas import VendaCreate, VendaBase, VendaResponse
from vendedor.model import ModeloVendedor
from sqlalchemy.orm import joinedload

router = APIRouter()

@router.get("/vendas", response_model=list[VendaBase])
def listar_vendas(db: Session = Depends(get_db)):
    return db.query(ModeloVenda).all()

@router.post("/vendas", response_model=VendaBase)
def adicionar_venda(venda: VendaCreate, db: Session = Depends(get_db)):
    cliente = db.query(ModeloCliente).filter(ModeloCliente.cpf == venda.cliente_cpf).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    vendedor = db.query(ModeloVendedor).filter(ModeloVendedor.cpf == venda.vendedor_cpf).first()
    if not vendedor:
        raise HTTPException(status_code=404, detail="Vendedor não encontrado")
    
    produto = db.query(ModeloProduto).filter(ModeloProduto.id == venda.produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    nova_venda = ModeloVenda(
        cliente_cpf=venda.cliente_cpf,
        vendedor_cpf=venda.vendedor_cpf,
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

@router.get("/vendas/cliente/{cpf}", response_model=list[VendaResponse])
def listar_vendas_por_cliente(cpf: str, db: Session = Depends(get_db)):
    vendas = db.query(ModeloVenda)\
        .options(
            joinedload(ModeloVenda.cliente),
            joinedload(ModeloVenda.vendedor),
            joinedload(ModeloVenda.produto),
        )\
        .filter(ModeloVenda.cliente_cpf == cpf)\
        .all()

    if not vendas:
        raise HTTPException(status_code=404, detail="Nenhuma venda encontrada para este CPF")

    return vendas