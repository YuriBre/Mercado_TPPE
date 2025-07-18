from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from cliente.router import router as clientes
from produto.router import router as produtos
from venda.router import router as vendas
from vendedor.router import router as vendedores

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(clientes, prefix="/clientes", tags=["Clientes"])
app.include_router(produtos, prefix="/produtos", tags=["Produtos"])
app.include_router(vendas, prefix="/vendas", tags=["Vendas"])
app.include_router(vendedores, prefix="/vendedores", tags=["Vendedores"])

@app.get("/")
def root():
    return {"message": "Mercado API"}
