from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from core.database import Base

# Modelo de Cliente para o SQLAlchemy
class Cliente(Base):
    __tablename__ = "clientes"

    # Campos da tabela de clientes
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(index=True)
    telefone: Mapped[str] = mapped_column(index=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), index=True)

    # Relacionamento com a tabela de agendamentos
    agendamentos = relationship("Agendamento", back_populates="cliente")
