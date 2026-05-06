from sqlalchemy.orm import Session
from .models import Cliente


def criar_cliente(db: Session, nome: str, email: str, telefone: str) -> Cliente:
    """Insere um novo cliente no banco de dados."""
    cliente = Cliente(nome=nome, email=email, telefone=telefone)
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente


def listar_clientes(db: Session) -> list[Cliente]:
    """Retorna todos os clientes cadastrados."""
    return db.query(Cliente).all()


def obter_cliente(db: Session, cliente_id: int) -> Cliente | None:
    """Busca um cliente pelo ID."""
    return db.query(Cliente).filter(Cliente.id == cliente_id).first()
