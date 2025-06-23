CREATE DATABASE IF NOT EXISTS mercado;
USE mercado;

-- Tabela Cliente
CREATE TABLE IF NOT EXISTS cliente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    endereco VARCHAR(150) NOT NULL,
    telefone VARCHAR(20) NOT NULL
);

-- Tabela Produto
CREATE TABLE IF NOT EXISTS produto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(255) NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    lucro_percentual DECIMAL(5,2) NOT NULL,
    qtd_estoque INT NOT NULL
);

-- Tabela Venda
CREATE TABLE IF NOT EXISTS venda (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    produto_id INT NOT NULL,
    quantidade INT NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES cliente(id),
    FOREIGN KEY (produto_id) REFERENCES produto(id)
);
