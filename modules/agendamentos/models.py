from sqlachemy import Column, Integer, String, DateTime, ForeignKey
from core.database import Base
from sqlalchemy.orm import relationship

# Modelo de Agendamento
class Agendamento(Base):
    __tablename__ = "agendamentos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    data = Column(DateTime, nullable=False)
    servico = Column(String, nullable=False)

    cliente = relationship("Cliente", back_populates="agendamentos")