from pydantic import BaseModel, field_validator
import re

# Schemas para clientes
class ClienteBase(BaseModel):
    nome: str
    telefone: str

    # Validações para os campos de cliente
    @field_validator("nome")
    @classmethod
    def nome_nao_vazio(cls, v: str) -> str:
        """Valida que o nome do cliente não seja vazio."""
        if not v.strip():
            raise ValueError("O nome do cliente não pode ser vazio")
        return v

    # Validação para o campo de telefone do cliente
    @field_validator("telefone")
    @classmethod
    def telefone_valido(cls, v: str) -> str:
        """Valida que o telefone do cliente seja um número válido."""
        if not v.isdigit() or len(v) < 8:
            raise ValueError("O telefone do cliente deve conter apenas dígitos e ter pelo menos 8 caracteres")
        return v

# Dados necessários para criar um novo cliente
class ClienteCreate(ClienteBase):
    """Dados necessários para criar um novo cliente."""
    pass

# Dados para atualizar um cliente existente
class ClienteUpdate(ClienteBase):
    """Dados para atualizar um cliente existente."""
    nome: str | None = None
    telefone: str | None = None

# Estrutura de resposta para cliente
class ClienteResponse(ClienteBase):
    """Estrutura de resposta de cliente."""
    id: int

# Configuração para permitir a conversão de objetos ORM para modelos Pydantic
class Config:
    orm_mode = True