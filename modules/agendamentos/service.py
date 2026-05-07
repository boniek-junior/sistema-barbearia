from sqlalchemy.orm import Session
from . import repository

# Função para criar um novo agendamento
def criar_agendamento(db: Session, cliente_id: int, data, servico: str):
    """Cria um novo agendamento."""
    return repository.criar_agendamento(db, cliente_id, data, servico)

# Função para listar todos os agendamentos
def listar_agendamentos(db: Session):
    """Retorna a lista de agendamentos cadastrados."""
    return repository.listar_agendamentos(db)