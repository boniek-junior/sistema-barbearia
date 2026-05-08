import enum


class StatusAgendamento(str, enum.Enum):
    pendente = "pendente"
    confirmado = "confirmado"
    concluido = "concluido"
    cancelado = "cancelado"