from datetime import datetime
from pydantic import BaseModel

class AgendamentoBase(BaseModel):
    cliente_id: int
    data: datetime
    servico: str

class AgendamentoCreate(AgendamentoBase):
    """Dados necessários para criar um agendamento."""
    pass

class AgendamentoResponse(AgendamentoBase):
    """Modelo de resposta para um agendamento."""
    id: int

class Config:
    orm_mode = True