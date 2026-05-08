from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.database import Base

# Modelo de Cliente para o SQLAlchemy
class Cliente(Base):
    __tablename__ = "clientes"

    # Campos da tabela de clientes
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    telefone = Column(String, index=True)

    # Relacionamento com a tabela de agendamentos
    agendamento = relationship("Agendamento", back_populates="cliente")