-- Tabela Cliente
CREATE TABLE IF NOT EXISTS cliente (
    cpf VARCHAR(11) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    endereco VARCHAR(150) NOT NULL,
    telefone VARCHAR(20) NOT NULL
);
-- Tabela Vendedor
CREATE TABLE IF NOT EXISTS vendedor (
    cpf VARCHAR(11) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    telefone VARCHAR(20) NOT NULL
);
-- Tabela Produto
CREATE TABLE IF NOT EXISTS produto (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(255) NOT NULL,
    valor NUMERIC(10, 2) NOT NULL,
    lucro_percentual NUMERIC(5, 2) NOT NULL,
    qtd_estoque INTEGER NOT NULL
);
-- Tabela Venda
CREATE TABLE IF NOT EXISTS venda (
    id SERIAL PRIMARY KEY,
    cliente_cpf VARCHAR(11) NOT NULL,
    produto_id INTEGER NOT NULL,
    vendedor_cpf VARCHAR(11) NOT NULL,
    quantidade INTEGER NOT NULL,
    valor_total NUMERIC(10, 2) NOT NULL,
    FOREIGN KEY (cliente_cpf) REFERENCES cliente(cpf),
    FOREIGN KEY (produto_id) REFERENCES produto(id),
    FOREIGN KEY (vendedor_cpf) REFERENCES vendedor(cpf)
);