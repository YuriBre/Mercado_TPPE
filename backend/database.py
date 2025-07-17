from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://mercado_jghe_user:NuB8IqLQg4PyThnG8jPQhNMlfVw6KE2T@dpg-d1sis215pdvs7397dr10-a.oregon-postgres.render.com:5432/mercado_jghe?sslmode=require"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Retorna uma sessão de banco de dados.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()