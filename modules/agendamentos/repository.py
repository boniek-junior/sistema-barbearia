from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from .models import Agendamento
from .status_enum import StatusAgendamento

class AgendamentoRepository:

    def buscar_conflito(self, db: Session, inicio: datetime, fim: datetime, ignorar_id: int = None) -> bool:
        """
        Verifica se existe algum agendamento ativo que se sobrepõe ao intervalo pedido.
        Fórmula: inicio_novo < fim_existente AND fim_novo > inicio_existente
        """
        query = db.query(Agendamento).filter(
            and_(
                Agendamento.inicio < fim,
                Agendamento.fim > inicio,
                Agendamento.status.notin_([StatusAgendamento.cancelado, StatusAgendamento.concluido])
            )
        )
        if ignorar_id is not None:
            query = query.filter(Agendamento.id != ignorar_id)

        return query.first() is not None

    def criar(self, db: Session, agendamento: Agendamento) -> Agendamento:
        db.add(agendamento)
        try:
            db.commit()
            db.refresh(agendamento)
            return agendamento
        except SQLAlchemyError:
            db.rollback()
            raise

    def listar_por_data(self, db: Session, data: datetime, skip: int = 0, limit: int = 100) -> list[Agendamento]:
        inicio_dia = data.replace(hour=0, minute=0, second=0, microsecond=0)
        fim_dia = data.replace(hour=23, minute=59, second=59, microsecond=999999)
        return db.query(Agendamento).filter(
            Agendamento.inicio >= inicio_dia,
            Agendamento.inicio <= fim_dia
        ).offset(skip).limit(limit).all()

    def listar_todos(self, db: Session, skip: int = 0, limit: int = 100) -> list[Agendamento]:
        return db.query(Agendamento).offset(skip).limit(limit).all()

    def buscar_por_id(self, db: Session, agendamento_id: int) -> Agendamento | None:
        return db.query(Agendamento).filter(Agendamento.id == agendamento_id).first()

    def atualizar_status(self, db: Session, agendamento: Agendamento, novo_status: StatusAgendamento) -> Agendamento:
        agendamento.status = novo_status
        db.commit()
        db.refresh(agendamento)
        return agendamento

    def deletar(self, db: Session, agendamento: Agendamento) -> None:
        db.delete(agendamento)
        db.commit()