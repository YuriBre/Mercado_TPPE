from database import Base, engine

# Cria as tabelas no banco de dados
print("Criando tabelas no banco de dados...")
Base.metadata.create_all(bind=engine)
print("Tabelas criadas com sucesso!")