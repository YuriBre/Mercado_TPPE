import asyncio
from fastapi import FastAPI
from databases import Database

DATABASE_URL = "mysql+aiomysql://user:user123@db:3306/mercado"
database = Database(DATABASE_URL)

app = FastAPI()

async def connect_with_retry():
    for attempt in range(10):
        try:
            await database.connect()
            print("Conectado ao banco!")
            return
        except Exception as e:
            print(f"Tentativa {attempt + 1} falhou: {e}")
            await asyncio.sleep(3)
    raise Exception("Não foi possível conectar ao banco após várias tentativas")

@app.on_event("startup")
async def startup():
    await connect_with_retry()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
async def root():
    return {"message": "API funcionando!"}

@app.post("/produtos/")
async def inserir_produto(nome: str, preco: int, quantidade: int):
    query = "INSERT INTO produtos (nome, preco, quantidade) VALUES (:nome, :preco, :quantidade)"
    await database.execute(query, values={"nome": nome, "preco": preco, "quantidade": quantidade})
    return {"message": "Produto inserido com sucesso!"}

@app.get("/produtos/")
async def listar_produtos():
    query = "SELECT * FROM produtos"
    produtos = await database.fetch_all(query)
    return {"produtos": produtos}

@app.delete("/produtos/{produto_id}")
async def deletar_produto(produto_id: int):
    query = "DELETE FROM produtos WHERE id = :produto_id"
    await database.execute(query, values={"produto_id": produto_id})
    return {"message": "Produto deletado com sucesso!"}