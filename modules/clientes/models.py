from sqlalchemy import Column, Integer, String
from core.database import Base

# Modelo de Cliente para o SQLAlchemy
class Cliente(Base):
    __tablename__ = "clientes"

    # Campos da tabela de clientes
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    telefone = Column(String, index=True)