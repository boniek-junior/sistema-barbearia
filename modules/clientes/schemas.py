from pydantic import BaseModel


class ClienteBase(BaseModel):
    nome: str
    email: str
    telefone: str


class ClienteCreate(ClienteBase):
    """Dados necessários para criar um novo cliente."""
    pass


class ClienteResponse(ClienteBase):
    """Estrutura de resposta de cliente."""
    id: int

    class Config:
        orm_mode = True
