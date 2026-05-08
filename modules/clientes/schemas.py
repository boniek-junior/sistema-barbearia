from pydantic import BaseModel

# Schemas para clientes
class ClienteBase(BaseModel):
    nome: str
    email: str
    telefone: str

# Dados necessários para criar um novo cliente
class ClienteCreate(ClienteBase):
    """Dados necessários para criar um novo cliente."""
    pass

# Estrutura de resposta para cliente
class ClienteResponse(ClienteBase):
    """Estrutura de resposta de cliente."""
    id: int

# Configuração para permitir a conversão de objetos ORM para modelos Pydantic
class Config:
    orm_mode = True