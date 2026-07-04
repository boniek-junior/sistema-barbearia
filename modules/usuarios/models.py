from sqlalchemy.orm import Mapped, mapped_column
from core.database import Base


# Modelo de Usuário para o SQLAlchemy
class Usuario(Base):
    __tablename__ = "usuarios"

    # Campos da tabela de usuários
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    senha_hash: Mapped[str] = mapped_column()