from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from core.database import Base
from .status_enum import StatusAgendamento
from .servicos_enum import TipoServico


class Agendamento(Base):
    __tablename__ = "agendamentos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id"), nullable=False)

    servico: Mapped[TipoServico] = mapped_column(
        Enum(TipoServico, name="tipo_servico_enum"),
        nullable=False
    )

    inicio: Mapped[datetime] = mapped_column(nullable=False)
    fim: Mapped[datetime] = mapped_column(nullable=False)

    status: Mapped[StatusAgendamento] = mapped_column(
        Enum(StatusAgendamento, name="status_agendamento_enum"),
        default=StatusAgendamento.pendente,
        nullable=False
    )

    cliente = relationship("Cliente", back_populates="agendamentos")