import pytest
from fastapi.testclient import TestClient
from app import app
import random

client = TestClient(app)

def criar_cliente():
    cpf = f"{random.randint(10000000000, 99999999999)}"
    cliente = {
        "cpf": cpf,
        "nome": "Cliente Teste",
        "endereco": "Rua Teste",
        "telefone": "11999999999"
    }
    response = client.post("/clientes/clientes", json=cliente)
    assert response.status_code == 200
    return cliente

def criar_vendedor():
    cpf = f"{random.randint(10000000000, 99999999999)}"
    vendedor = {
        "cpf": cpf,
        "nome": "Vendedor Teste",
        "email": f"vendedor{random.randint(1000,9999)}@teste.com",
        "telefone": "11988888888"
    }
    response = client.post("/vendedores/vendedores", json=vendedor)
    assert response.status_code == 200
    return vendedor

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
    vendedor = criar_vendedor()
    produto = criar_produto()
    venda = {
        "cliente_cpf": cliente["cpf"],
        "vendedor_cpf": vendedor["cpf"],
        "produto_id": produto["id"],
        "quantidade": 2
    }
    return venda, cliente["cpf"], produto["id"], vendedor["cpf"]

def test_criar_venda(venda_dados):
    venda, cliente_cpf, produto_id, vendedor_cpf = venda_dados
    response = client.post("/vendas/vendas", json=venda)
    assert response.status_code == 200
    data = response.json()
    assert data["cliente_cpf"] == venda["cliente_cpf"]
    assert data["vendedor_cpf"] == venda["vendedor_cpf"]
    assert data["produto_id"] == venda["produto_id"]
    assert data["quantidade"] == venda["quantidade"]
    assert data["valor_total"] > 0

    # Cleanup
    client.delete(f"/vendas/vendas/{data['id']}")
    client.delete(f"/clientes/clientes/{cliente_cpf}")
    client.delete(f"/produtos/produtos/{produto_id}")
    client.delete(f"/vendedores/vendedores/{vendedor_cpf}")

def test_listar_vendas(venda_dados):
    venda, cliente_cpf, produto_id, vendedor_cpf = venda_dados
    response = client.post("/vendas/vendas", json=venda)
    assert response.status_code == 200
    venda_id = response.json()["id"]

    lista = client.get("/vendas/vendas")
    assert lista.status_code == 200
    assert any(v["id"] == venda_id for v in lista.json())

    # Cleanup
    client.delete(f"/vendas/vendas/{venda_id}")
    client.delete(f"/clientes/clientes/{cliente_cpf}")
    client.delete(f"/produtos/produtos/{produto_id}")
    client.delete(f"/vendedores/vendedores/{vendedor_cpf}")

def test_buscar_venda(venda_dados):
    venda, cliente_cpf, produto_id, vendedor_cpf = venda_dados
    response = client.post("/vendas/vendas", json=venda)
    assert response.status_code == 200
    venda_id = response.json()["id"]

    busca = client.get(f"/vendas/vendas/{venda_id}")
    assert busca.status_code == 200
    assert busca.json()["id"] == venda_id

    # Cleanup
    client.delete(f"/vendas/vendas/{venda_id}")
    client.delete(f"/clientes/clientes/{cliente_cpf}")
    client.delete(f"/produtos/produtos/{produto_id}")
    client.delete(f"/vendedores/vendedores/{vendedor_cpf}")

def test_remover_venda(venda_dados):
    venda, cliente_cpf, produto_id, vendedor_cpf = venda_dados
    response = client.post("/vendas/vendas", json=venda)
    assert response.status_code == 200
    venda_id = response.json()["id"]

    delete = client.delete(f"/vendas/vendas/{venda_id}")
    assert delete.status_code == 200
    assert delete.json()["message"] == "Venda removida com sucesso!"

    buscar = client.get(f"/vendas/vendas/{venda_id}")
    assert buscar.status_code == 404

    # Cleanup
    client.delete(f"/clientes/clientes/{cliente_cpf}")
    client.delete(f"/produtos/produtos/{produto_id}")
    client.delete(f"/vendedores/vendedores/{vendedor_cpf}")
