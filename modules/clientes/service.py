from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import repository
from .validator import ClienteValidator

_validator = ClienteValidator()

def criar_cliente(db: Session, nome: str, telefone: str, usuario_id: int):
    """Cria um cliente vinculado ao usuario logado."""
    _validator.validar_nome(nome)
    _validator.validar_telefone_unico(db, telefone, usuario_id)
    return repository.criar_cliente(db, nome, telefone, usuario_id)

def listar_clientes(db: Session, usuario_id: int):
    """Retorna a lista de clientes do usuario logado."""
    return repository.listar_clientes(db, usuario_id)

def obter_cliente(db: Session, cliente_id: int, usuario_id: int):
    """Retorna um cliente do usuario logado pelo ID."""
    return repository.obter_cliente(db, cliente_id, usuario_id)

def atualizar_cliente(db: Session, cliente_id: int, dados: dict, usuario_id: int):
    """Atualiza os dados de um cliente existente, apos validar as regras de negocio."""
    cliente = repository.obter_cliente(db, cliente_id, usuario_id)
    if cliente is None:
        return None

    if "nome" in dados and dados["nome"] is not None:
        _validator.validar_nome(dados["nome"])

    if "telefone" in dados and dados["telefone"] is not None:
        _validator.validar_telefone_unico(db, dados["telefone"], usuario_id, ignorar_id=cliente_id)

    return repository.atualizar_cliente(db, cliente, dados)

def deletar_cliente(db: Session, cliente_id: int, usuario_id: int):
    """Deleta um cliente do usuario logado."""
    cliente = repository.obter_cliente(db, cliente_id, usuario_id)
    if cliente is None:
        raise HTTPException(
            status_code=404,
            detail="Cliente nao encontrado"
            )

    sucesso = repository.deletar_cliente(db, cliente)
    if not sucesso:
        raise HTTPException(
            status_code=400,
            detail="Nao e possivel excluir o cliente pois ele possui agendamentos vinculados."
        )
    return cliente
