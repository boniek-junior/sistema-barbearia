from sqlalchemy.orm import Session
from . import repository

# Serviços para criar clientes
def criar_cliente(db: Session, nome: str, telefone: str):
    """Cria um cliente e delega a persistência ao repositório."""
    return repository.criar_cliente(db, nome, telefone)

# Serviços para listar clientes
def listar_clientes(db: Session):
    """Retorna a lista de clientes cadastrados."""
    return repository.listar_clientes(db)

# Serviços para obter um cliente pelo ID
def obter_cliente(db: Session, cliente_id: int):
    """Retorna um cliente pelo ID."""
    return repository.obter_cliente(db, cliente_id)

# Serviços para atualizar um cliente existente
def atualizar_cliente(db: Session, cliente_id: int, dados: dict):
    """Atualiza os dados de um cliente existente."""
    cliente = repository.obter_cliente(db, cliente_id)
    if cliente is None:
        return None
    return repository.atualizar_cliente(db, cliente, dados)

# Serviços para deletar um cliente
def deletar_cliente(db: Session, cliente_id: int):
    """Deleta um cliente do banco de dados."""
    cliente = repository.obter_cliente(db, cliente_id)
    if cliente is None:
        return False
    repository.deletar_cliente(db, cliente)
    return True