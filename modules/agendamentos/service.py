from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends

from core.config import settings
from .models import Agendamento
from .schemas import AgendamentoCreate
from .repository import AgendamentoRepository
from .servicos_enum import TipoServico
from .status_enum import StatusAgendamento


class AgendamentoService:
    def __init__(self, repository: AgendamentoRepository = Depends()):
        self.repository = repository

    def _validar_horario_funcionamento(self, inicio: datetime, fim: datetime) -> None:

        abertura = inicio.replace(
            hour=settings.HORARIO_ABERTURA,
            minute=0,
            second=0,
            microsecond=0
        )

        fechamento = inicio.replace(
            hour=settings.HORARIO_FECHAMENTO,
            minute=0,
            second=0,
            microsecond=0
        )

        if inicio < abertura or fim > fechamento:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Agendamentos apenas entre "
                    f"{settings.HORARIO_ABERTURA:02d}:00 e "
                    f"{settings.HORARIO_FECHAMENTO:02d}:00."
                )
            )

    def _obter_duracao_servico(self, servico: TipoServico) -> int:
        try:
            return servico.duracao_minutos
        
        except AttributeError:
            
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Serviço inválido."
         )

     

    def criar_agendamento(self, db: Session, dados: AgendamentoCreate) -> Agendamento:

        agora = datetime.now(dados.inicio.tzinfo) if dados.inicio.tzinfo else datetime.now()
        if dados.inicio < agora:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não é possível agendar para um horário no passado."
            )

        duracao = self._obter_duracao_servico(dados.servico)

        fim = dados.inicio + timedelta(minutes=duracao)

        self._validar_horario_funcionamento(dados.inicio, fim)

        conflito = self.repository.buscar_conflito(db, dados.inicio, fim)

        if conflito:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Horário indisponível. Por favor, escolha outro horário."
            )

        novo_agendamento = Agendamento(
            cliente_id=dados.cliente_id,
            servico=dados.servico,
            inicio=dados.inicio,
            fim=fim,
            status=StatusAgendamento.pendente
        )

        return self.repository.criar(db, novo_agendamento)

    def listar_agendamentos(self, db: Session, data: datetime | None = None, skip: int = 0, limit: int = 100):
        if data:
            return self.repository.listar_por_data(db, data, skip, limit)
        return self.repository.listar_todos(db, skip, limit)

    def buscar_por_id(self, db: Session, agendamento_id: int) -> Agendamento:
        agendamento = self.repository.buscar_por_id(db, agendamento_id)
        if not agendamento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agendamento não encontrado."
            )
        return agendamento

    def atualizar_status(self, db: Session, agendamento_id: int, novo_status: StatusAgendamento) -> Agendamento:
        agendamento = self.buscar_por_id(db, agendamento_id)
        return self.repository.atualizar_status(db, agendamento, novo_status)

    def deletar_agendamento(self, db: Session, agendamento_id: int) -> None:
        agendamento = self.buscar_por_id(db, agendamento_id)
        self.repository.deletar(db, agendamento)