import pytest
from fastapi.testclient import TestClient
from app import app
import random

client = TestClient(app)

def criar_cliente():
    cliente = {
        "id": random.randint(10000, 99999),
        "nome": "Cliente Teste",
        "endereco": "Rua Teste",
        "telefone": "11999999999"
    }
    response = client.post("/clientes/clientes", json=cliente)
    assert response.status_code == 200
    return cliente

def criar_produto():
    produto = {
        "nome": f"Produto {random.randint(1000, 9999)}",
        "descricao": "Produto de teste",
        "valor": 10.0,
        "lucro_percentual": 20.0,
        "qtd_estoque": 100
    }
    response = client.post("/produtos/produtos", json=produto)
    assert response.status_code == 200
    return response.json()

@pytest.fixture
def venda_dados():
    cliente = criar_cliente()
    produto = criar_produto()
    venda = {
        "cliente_id": cliente["id"],
        "produto_id": produto["id"],
        "quantidade": 2
    }
    return venda, cliente["id"], produto["id"]

def test_criar_venda(venda_dados):
    venda, cliente_id, produto_id = venda_dados
    response = client.post("/vendas/vendas", json=venda)
    assert response.status_code == 200
    data = response.json()
    assert data["cliente_id"] == venda["cliente_id"]
    assert data["produto_id"] == venda["produto_id"]
    assert data["quantidade"] == venda["quantidade"]
    assert data["valor_total"] > 0
    client.delete(f"/vendas/vendas/{data['id']}")
    client.delete(f"/clientes/clientes/{cliente_id}")
    client.delete(f"/produtos/produtos/{produto_id}")

def test_listar_vendas(venda_dados):
    venda, cliente_id, produto_id = venda_dados
    response = client.post("/vendas/vendas", json=venda)
    assert response.status_code == 200
    venda_id = response.json()["id"]

    lista = client.get("/vendas/vendas")
    assert lista.status_code == 200
    assert any(v["id"] == venda_id for v in lista.json())

    client.delete(f"/vendas/vendas/{venda_id}")
    client.delete(f"/clientes/clientes/{cliente_id}")
    client.delete(f"/produtos/produtos/{produto_id}")

def test_buscar_venda(venda_dados):
    venda, cliente_id, produto_id = venda_dados
    response = client.post("/vendas/vendas", json=venda)
    assert response.status_code == 200
    venda_id = response.json()["id"]

    busca = client.get(f"/vendas/vendas/{venda_id}")
    assert busca.status_code == 200
    assert busca.json()["id"] == venda_id

    client.delete(f"/vendas/vendas/{venda_id}")
    client.delete(f"/clientes/clientes/{cliente_id}")
    client.delete(f"/produtos/produtos/{produto_id}")

def test_remover_venda(venda_dados):
    venda, cliente_id, produto_id = venda_dados
    response = client.post("/vendas/vendas", json=venda)
    assert response.status_code == 200
    venda_id = response.json()["id"]

    delete = client.delete(f"/vendas/vendas/{venda_id}")
    assert delete.status_code == 200
    assert delete.json()["message"] == "Venda removida com sucesso!"

    buscar = client.get(f"/vendas/vendas/{venda_id}")
    assert buscar.status_code == 404

    client.delete(f"/clientes/clientes/{cliente_id}")
    client.delete(f"/produtos/produtos/{produto_id}")
