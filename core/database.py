from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from core.config import settings

# Configuração do banco de dados

connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)

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