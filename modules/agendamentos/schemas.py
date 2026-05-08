from pydantic import BaseModel, field_validator
from datetime import datetime
from .status_enum import StatusAgendamento
from .servicos_enum import TipoServico

class AgendamentoCreate(BaseModel):
    cliente_id: int
    inicio: datetime
    servico: TipoServico

    @field_validator("inicio")
    @classmethod
    def validar_data(cls, v: datetime):
        agora = datetime.now(v.tzinfo) if v.tzinfo else datetime.now()
        if v < agora:
            raise ValueError("Não é possível agendar em datas passadas.")
        return v

class AgendamentoUpdate(BaseModel):
    status: StatusAgendamento

class AgendamentoResponse(BaseModel):
    id: int
    cliente_id: int
    servico: TipoServico
    inicio: datetime
    fim: datetime
    status: StatusAgendamento

    model_config = {"from_attributes": True}