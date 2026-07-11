from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from . import repository

# Validator para clientes
class ClienteValidator:
    """Valida regras de negocio relacionadas a clientes."""

    # Valida que o telefone do cliente seja unico entre os clientes do mesmo usuario
    def validar_telefone_unico(self, db: Session, telefone: str, usuario_id: int, ignorar_id: int | None = None) -> None:
        """Valida que o telefone do cliente seja unico entre os clientes do usuario logado."""

        cliente_existente = repository.obter_cliente_por_telefone(db, telefone, usuario_id)

        if cliente_existente is None:
            return

        if ignorar_id is not None and cliente_existente.id == ignorar_id:
            return

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ja existe um cliente com o telefone {telefone}."
            )

    # Valida que o nome do cliente nao seja vazio
    def validar_nome(self, nome: str) -> None:
        """Valida que o nome do cliente contenha nome e sobrenome."""
        partes = nome.strip().split()
        if len(partes) < 2:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="O nome do cliente deve conter pelo menos nome e sobrenome."
                )
