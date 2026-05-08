from sqlalchemy.orm import Session
from .models import Cliente


# Função para criar um novo cliente no banco de dados
def criar_cliente(db: Session, nome: str, email: str, telefone: str) -> Cliente:
    """Insere um novo cliente no banco de dados."""

    cliente = Cliente(nome=nome, email=email, telefone=telefone)
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