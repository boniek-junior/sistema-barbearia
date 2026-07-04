from fastapi import APIRouter, Depends, status, Query
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import obter_usuario_atual
from . import schemas, service

router = APIRouter()

@router.post("/", response_model=schemas.AgendamentoResponse, status_code=status.HTTP_201_CREATED)
def criar_agendamento(
    agendamento: schemas.AgendamentoCreate,
    db: Session = Depends(get_db),
    svc: service.AgendamentoService = Depends(),
    usuario=Depends(obter_usuario_atual),
):
    """Cria um novo agendamento."""
    return svc.criar_agendamento(db, agendamento)

@router.get("/", response_model=list[schemas.AgendamentoResponse])
def listar_agendamentos(
    data: Optional[datetime] = Query(None, description="Filtra por data (ex: 2026-05-08T00:00:00)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db),
    svc: service.AgendamentoService = Depends(),
    usuario=Depends(obter_usuario_atual),
): 
    """Retorna agendamentos, opcionalmente filtrados por data e com paginação."""
    return svc.listar_agendamentos(db, data, skip, limit)


@router.get("/{agendamento_id}", response_model=schemas.AgendamentoResponse)
def buscar_agendamento(
    agendamento_id: int, 
    db: Session = Depends(get_db),
    svc: service.AgendamentoService = Depends(),
    usuario=Depends(obter_usuario_atual),
):
    """Busca um agendamento específico pelo ID."""
    return svc.buscar_por_id(db, agendamento_id)

@router.patch("/{agendamento_id}/status", response_model=schemas.AgendamentoResponse)
def atualizar_status(
    agendamento_id: int, 
    atualizacao: schemas.AgendamentoUpdate, 
    db: Session = Depends(get_db),
    svc: service.AgendamentoService = Depends(),
    usuario=Depends(obter_usuario_atual),
):
    """Atualiza o status de um agendamento existente."""
    return svc.atualizar_status(db, agendamento_id, atualizacao.status)

@router.delete("/{agendamento_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_agendamento(
    agendamento_id: int, 
    db: Session = Depends(get_db),
    svc: service.AgendamentoService = Depends(),
    usuario=Depends(obter_usuario_atual),
):
    """Exclui um agendamento do banco de dados."""
    svc.deletar_agendamento(db, agendamento_id)