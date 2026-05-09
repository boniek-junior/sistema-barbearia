from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .models import Cliente


# Função para criar um novo cliente no banco de dados
def criar_cliente(db: Session, nome: str, telefone: str) -> Cliente:
    """Insere um novo cliente no banco de dados."""

    cliente = Cliente(nome=nome, telefone=telefone)
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente

# Função para listar todos os clientes do banco de dados
def listar_clientes(db: Session) -> list[Cliente]:
    """Retorna todos os clientes cadastrados."""
    return db.query(Cliente).all()

# Função para obter um cliente pelo ID
def obter_cliente(db: Session, cliente_id: int) -> Cliente | None:
    """Busca um cliente pelo ID."""
    return db.query(Cliente).filter(Cliente.id == cliente_id).first()

# Função para atualizar os dados de um cliente existente
def atualizar_cliente(db: Session, cliente: Cliente, dados: dict) -> Cliente:
    """Atualiza os dados de um cliente existente."""
    for campo, valor in dados.items():
        if valor is not None:
            setattr(cliente, campo, valor)
    db.commit()
    db.refresh(cliente)
    return cliente

# Função para deletar um cliente do banco de dados
def deletar_cliente(db: Session, cliente: Cliente) -> bool:
    """Remove um cliente do banco de dados."""
    db.delete(cliente)
    try:
        db.commit()
        return True
    except IntegrityError:
        db.rollback()
        return False