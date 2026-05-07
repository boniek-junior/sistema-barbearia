from sqlalchemy.orm import Session
from . import repository

# Serviços para criar clientes
def criar_cliente(db: Session, nome: str, email: str, telefone: str):
    """Cria um cliente e delega a persistência ao repositório."""
    return repository.criar_cliente(db, nome, email, telefone)

# Serviços para listar clientes
def listar_clientes(db: Session):
    """Retorna a lista de clientes cadastrados."""
    return repository.listar_clientes(db)

# Serviços para obter um cliente pelo ID
def obter_cliente(db: Session, cliente_id: int):
    """Retorna um cliente pelo ID."""
    return repository.obter_cliente(db, cliente_id)
