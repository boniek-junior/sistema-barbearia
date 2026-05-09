from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from . import repository

# Validator para clientes
class ClienteValidator:
    """Valida regras de negócio relacionadas a clientes.

    Responsabilidades:
    - Validar unicidade do telefone do cliente
    - Validar preenchimento do nome do cliente

    NÃO é responsavel por validar formatos de dados (isso é responsabilidade dos schemas) 
    ou por regras de negócio relacionadas a agendamentos (isso é responsabilidade do módulo de agendamento)."""

    # Valida que o telefone do cliente seja único no banco de dados
    def validar_telefone_unico(self, db: Session, telefone: str, ignorar_id: int | None = None) -> None:
        """Valida que o telefone do cliente seja único no banco de dados."""
        
        cliente_existente = repository.obter_cliente_por_telefone(db, telefone)

        if cliente_existente is None: 
            return
        
        if ignorar_id is not None and cliente_existente.id == ignorar_id:
            return

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail=f"Já existe um cliente com o telefone {telefone}."
            )
    
    # Valida que o nome do cliente não seja vazio
    def validar_nome(self, nome: str) -> None:

        """Valida que o nome do cliente não seja vazio.
        Além disso, valida que o nome contenha pelo menos um sobrenome para garantir uma identificação mais clara do cliente."""
        partes = nome.strip().split()
        if len(partes) < 2:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                detail="O nome do cliente deve conter pelo menos nome e sobrenome."
                )