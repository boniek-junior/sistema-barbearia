from pydantic import BaseModel, EmailStr, field_validator

#Schema base de usuário
class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr

# Dados necessários para criar um novo usuário
class UsuarioCreate(UsuarioBase):
    """Dados necessários para criar um novo usuário."""
    senha: str

    @field_validator("senha")
    @classmethod
    def validar_senha(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("A senha deve ter pelo menos 6 caracteres")
        return v
    
    @field_validator("nome")
    @classmethod
    def validar_nome(cls, v: str) -> str:
        if len(v) < 2:
            raise ValueError("O nome deve ter pelo menos 2 caracteres")
        return v
    
# Dados retornados ao cliente após a criação de um usuário
class UsuarioResponse(UsuarioBase):
    """Dados retornados ao cliente após a criação de um usuário."""
    id: int

    model_config = {
        "from_attributes": True  # Permite que o Pydantic trabalhe com objetos ORM do SQLAlchemy
    }

class Token(BaseModel):
    """Modelo para o token JWT retornado após o login."""
    access_token: str
    token_type: str = "bearer"

    class Config:
        orm_mode = True