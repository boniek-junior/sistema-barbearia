from sqlalchemy.orm import Session
from .models import Agendamento

# Função para criar um novo agendamento
def criar_agendamento(db: Session, cliente_id: int, data, servico: str):
    """Cria um novo agendamento no banco de dados."""
    agendamento = Agendamento(
        cliente_id=cliente_id,
        data=data,
        servico=servico,
    )
    db.add(agendamento)
    db.commit()
    db.refresh(agendamento)
    return agendamento

# Função para listar todos os agendamentos
def listar_agendamentos(db: Session):
    """Retorna todos os agendamentos cadastrados."""
    return db.query(Agendamento).all()