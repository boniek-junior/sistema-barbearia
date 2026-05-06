from sqlalchemy.orm import Session
from . import repository


def criar_cliente(db: Session, nome: str, email: str, telefone: str):
    """Cria um cliente e delega a persistência ao repositório."""
    return repository.criar_cliente(db, nome, email, telefone)


def listar_clientes(db: Session):
    """Retorna a lista de clientes cadastrados."""
    return repository.listar_clientes(db)


def obter_cliente(db: Session, cliente_id: int):
    """Retorna um cliente pelo ID."""
    return repository.obter_cliente(db, cliente_id)
