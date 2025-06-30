from fastapi import FastAPI
from cliente.router import router as clientes
from produto.router import router as produtos
from venda.router import router as vendas
from pagamento.router import router as pagamentos

app = FastAPI()

app.include_router(clientes, prefix="/clientes", tags=["Clientes"])
app.include_router(produtos, prefix="/produtos", tags=["Produtos"])
app.include_router(vendas, prefix="/vendas", tags=["Vendas"])
app.include_router(pagamentos, prefix="/pagamentos", tags=["Pagamentos"])

@app.get("/")
def root():
    return {"message": "Mercado API"}