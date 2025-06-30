import pytest
from fastapi.testclient import TestClient
from app import app
import random

client = TestClient(app)

def criar_cliente():
    cliente = {
        "id": random.randint(100000, 999999),
        "nome": "Cliente Teste",
        "endereco": "Rua Teste",
        "telefone": "11999999999"
    }
    resp = client.post("/clientes/clientes", json=cliente)
    assert resp.status_code == 200
    return cliente

def criar_produto():
    produto = {
        "nome": f"Produto Teste {random.randint(1000, 9999)}",
        "descricao": "Descrição de teste",
        "valor": 20.0,
        "lucro_percentual": 15.0,
        "qtd_estoque": 50
    }
    resp = client.post("/produtos/produtos", json=produto)
    assert resp.status_code == 200
    return resp.json()

def criar_venda(cliente_id, produto_id):
    venda = {
        "cliente_id": cliente_id,
        "produto_id": produto_id,
        "quantidade": 1
    }
    resp = client.post("/vendas/vendas", json=venda)
    assert resp.status_code == 200
    return resp.json()

@pytest.fixture
def dados_pagamento():
    cliente = criar_cliente()
    produto = criar_produto()
    venda = criar_venda(cliente["id"], produto["id"])
    pagamento = {
        "venda_id": venda["id"],
        "valor_pago": venda["valor_total"],
        "metodo_pagamento": "pix"
    }
    return pagamento, cliente["id"], produto["id"], venda["id"]

def test_criar_pagamento(dados_pagamento):
    pagamento, cliente_id, produto_id, venda_id = dados_pagamento
    resp = client.post("/pagamentos/pagamentos", json=pagamento)
    assert resp.status_code == 200
    data = resp.json()
    assert data["venda_id"] == pagamento["venda_id"]
    assert float(data["valor_pago"]) == float(pagamento["valor_pago"])
    assert data["metodo_pagamento"] == pagamento["metodo_pagamento"]
    assert "data_pagamento" in data

    # Cleanup
    client.delete(f"/pagamentos/pagamentos/{data['id']}")
    client.delete(f"/vendas/vendas/{venda_id}")
    client.delete(f"/clientes/clientes/{cliente_id}")
    client.delete(f"/produtos/produtos/{produto_id}")

def test_listar_pagamentos(dados_pagamento):
    pagamento, cliente_id, produto_id, venda_id = dados_pagamento
    resp = client.post("/pagamentos/pagamentos", json=pagamento)
    assert resp.status_code == 200
    pag_id = resp.json()["id"]

    lista = client.get("/pagamentos/pagamentos")
    assert lista.status_code == 200
    assert any(p["id"] == pag_id for p in lista.json())

    # Cleanup
    client.delete(f"/pagamentos/pagamentos/{pag_id}")
    client.delete(f"/vendas/vendas/{venda_id}")
    client.delete(f"/clientes/clientes/{cliente_id}")
    client.delete(f"/produtos/produtos/{produto_id}")

def test_buscar_pagamento(dados_pagamento):
    pagamento, cliente_id, produto_id, venda_id = dados_pagamento
    resp = client.post("/pagamentos/pagamentos", json=pagamento)
    assert resp.status_code == 200
    pag_id = resp.json()["id"]

    busca = client.get(f"/pagamentos/pagamentos/{pag_id}")
    assert busca.status_code == 200
    assert busca.json()["id"] == pag_id

    # Cleanup
    client.delete(f"/pagamentos/pagamentos/{pag_id}")
    client.delete(f"/vendas/vendas/{venda_id}")
    client.delete(f"/clientes/clientes/{cliente_id}")
    client.delete(f"/produtos/produtos/{produto_id}")

def test_remover_pagamento(dados_pagamento):
    pagamento, cliente_id, produto_id, venda_id = dados_pagamento
    resp = client.post("/pagamentos/pagamentos", json=pagamento)
    assert resp.status_code == 200
    pag_id = resp.json()["id"]

    delete = client.delete(f"/pagamentos/pagamentos/{pag_id}")
    assert delete.status_code == 200

    busca = client.get(f"/pagamentos/pagamentos/{pag_id}")
    assert busca.status_code == 404

    # Cleanup
    client.delete(f"/vendas/vendas/{venda_id}")
    client.delete(f"/clientes/clientes/{cliente_id}")
    client.delete(f"/produtos/produtos/{produto_id}")
