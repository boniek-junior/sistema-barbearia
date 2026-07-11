from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends

from core.config import settings
from .models import Agendamento
from .schemas import AgendamentoCreate
from .repository import AgendamentoRepository
from .servicos_enum import TipoServico
from .status_enum import StatusAgendamento
from modules.clientes.repository import obter_cliente


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
                detail="Servico invalido."
            )

    def criar_agendamento(self, db: Session, dados: AgendamentoCreate, usuario_id: int) -> Agendamento:
        cliente = obter_cliente(db, dados.cliente_id, usuario_id)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente nao encontrado."
            )

        agora = datetime.now(dados.inicio.tzinfo) if dados.inicio.tzinfo else datetime.now()
        if dados.inicio < agora:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nao e possivel agendar para um horario no passado."
            )

        duracao = self._obter_duracao_servico(dados.servico)
        fim = dados.inicio + timedelta(minutes=duracao)

        self._validar_horario_funcionamento(dados.inicio, fim)

        conflito = self.repository.buscar_conflito(db, dados.inicio, fim, usuario_id)
        if conflito:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Horario indisponivel. Por favor, escolha outro horario."
            )

        novo_agendamento = Agendamento(
            cliente_id=dados.cliente_id,
            servico=dados.servico,
            inicio=dados.inicio,
            fim=fim,
            status=StatusAgendamento.pendente
        )

        return self.repository.criar(db, novo_agendamento)

    def listar_agendamentos(self, db: Session, usuario_id: int, data: datetime | None = None, skip: int = 0, limit: int = 100):
        if data:
            return self.repository.listar_por_data(db, data, usuario_id, skip, limit)
        return self.repository.listar_todos(db, usuario_id, skip, limit)

    def buscar_por_id(self, db: Session, agendamento_id: int, usuario_id: int) -> Agendamento:
        agendamento = self.repository.buscar_por_id(db, agendamento_id, usuario_id)
        if not agendamento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agendamento nao encontrado."
            )
        return agendamento

    def atualizar_status(self, db: Session, agendamento_id: int, novo_status: StatusAgendamento, usuario_id: int) -> Agendamento:
        agendamento = self.buscar_por_id(db, agendamento_id, usuario_id)
        return self.repository.atualizar_status(db, agendamento, novo_status)

    def deletar_agendamento(self, db: Session, agendamento_id: int, usuario_id: int) -> None:
        agendamento = self.buscar_por_id(db, agendamento_id, usuario_id)
        self.repository.deletar(db, agendamento)
