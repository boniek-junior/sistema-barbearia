from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from . import schemas, service

#Roteador para agendamentos
router = APIRouter()

# Endpoint para criar um novo agendamento
@router.post("/", response_model=schemas.AgendamentoResponse)
def criar_agendamento(
    agendamento: schemas.AgendamentoCreate,
    db: Session = Depends(get_db),
):
    """Cria um novo agendamento."""
    return service.criar_agendamento(
        db,
        agendamento.cliente_id,
        agendamento.data,
        agendamento.servico,
    )

# Endpoint para listar todos os agendamentos
@router.get("/", response_model=list[schemas.AgendamentoResponse])
def listar_agendamentos(db: Session = Depends(get_db)): 
    """Retorna todos os agendamentos gerados."""
    return service.listar_agendamentos(db)