from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .models import Cliente


# Funcao para criar um novo cliente no banco de dados
def criar_cliente(db: Session, nome: str, telefone: str, usuario_id: int) -> Cliente:
    """Insere um novo cliente no banco de dados, vinculado ao usuario dono."""
    cliente = Cliente(nome=nome, telefone=telefone, usuario_id=usuario_id)
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente

# Funcao para listar todos os clientes de um usuario
def listar_clientes(db: Session, usuario_id: int) -> list[Cliente]:
    """Retorna os clientes cadastrados pelo usuario logado."""
    return db.query(Cliente).filter(Cliente.usuario_id == usuario_id).all()

# Funcao para obter um cliente pelo ID, restrito ao dono
def obter_cliente(db: Session, cliente_id: int, usuario_id: int) -> Cliente | None:
    """Busca um cliente pelo ID, apenas se pertencer ao usuario logado."""
    return db.query(Cliente).filter(
        Cliente.id == cliente_id,
        Cliente.usuario_id == usuario_id
    ).first()

# Funcao para obter um cliente pelo telefone, restrito ao dono
def obter_cliente_por_telefone(db: Session, telefone: str, usuario_id: int) -> Cliente | None:
    """Busca um cliente pelo telefone, apenas entre os clientes do usuario logado."""
    return db.query(Cliente).filter(
        Cliente.telefone == telefone,
        Cliente.usuario_id == usuario_id
    ).first()

# Funcao para atualizar os dados de um cliente existente
def atualizar_cliente(db: Session, cliente: Cliente, dados: dict) -> Cliente:
    """Atualiza os dados de um cliente existente."""
    for campo, valor in dados.items():
        if valor is not None:
            setattr(cliente, campo, valor)
    db.commit()
    db.refresh(cliente)
    return cliente

# Funcao para deletar um cliente do banco de dados
def deletar_cliente(db: Session, cliente: Cliente) -> bool:
    """Remove um cliente do banco de dados."""
    db.delete(cliente)
    try:
        db.commit()
        return True
    except IntegrityError:
        db.rollback()
        return False
