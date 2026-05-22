from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from core.config import settings

# Configuração do banco de dados
database_url = settings.DATABASE_URL
connect_args = {}
if database_url.startswith("sqlite"):
    # sqlite requires this arg for use with the same connection in multiple threads
    connect_args = {"check_same_thread": False}

engine = create_engine(database_url, connect_args=connect_args)

# Criando a sessão do SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criando a base para os modelos do SQLAlchemy
Base = declarative_base()

# Função para obter a sessão do banco de dados
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()