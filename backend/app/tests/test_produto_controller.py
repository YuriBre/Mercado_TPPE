from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_inserir_produto():
    response = client.post("/produtos/", json={"nome": "Produto Teste", "preco": 100, "quantidade": 10})
    assert response.status_code == 200
    assert response.json() == {"message": "Produto inserido com sucesso!"}

def test_listar_produtos():
    response = client.get("/produtos/")
    assert response.status_code == 200
    assert "produtos" in response.json()

def test_deletar_produto():
    response = client.delete("/produtos/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Produto deletado com sucesso!"}