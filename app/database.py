import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Pega a URL do banco de dados da variável de ambiente
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data.db")

# Define os argumentos de conexão dependendo do tipo de banco
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

# Cria o engine do SQLAlchemy
engine = create_engine(
    DATABASE_URL.replace("postgresql://", "postgresql+psycopg://"),
    pool_pre_ping=True
)


# Cria o Base e a Session
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Função para gerar sessões do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
