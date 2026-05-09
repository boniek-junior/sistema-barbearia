from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import repository
from .validator import ClienteValidator

_validator = ClienteValidator()

# Serviços para criar clientes
def criar_cliente(db: Session, nome: str, telefone: str):
    """Cria um cliente e delega a persistência ao repositório."""
    _validator.validar_nome(nome)
    _validator.validar_telefone_unico(db, telefone)
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
    """Atualiza os dados de um cliente existente após validar as regras de negócio."""
    cliente = repository.obter_cliente(db, cliente_id)
    if cliente is None:
        return None
    
    if "nome" in dados and dados["nome"] is not None:
        _validator.validar_nome(dados["nome"])
   
    if "telefone" in dados and dados["telefone"] is not None:
        _validator.validar_telefone_unico(db, dados["telefone"], ignorar_id=cliente_id)
   
    return repository.atualizar_cliente(db, cliente, dados)

# Serviços para deletar um cliente
def deletar_cliente(db: Session, cliente_id: int):
    """Deleta um cliente do banco de dados."""
    cliente = repository.obter_cliente(db, cliente_id)
    if cliente is None:
        raise HTTPException(
            status_code=404, 
            detail="Cliente não encontrado"
            )
    
    sucesso = repository.deletar_cliente(db, cliente)
    if not sucesso:
        raise HTTPException(
            status_code=400,
            detail="Não é possível excluir o cliente pois ele possui agendamentos vinculados."
        )
    return cliente # Retorna o cliente deletado para fins de resposta, embora a rota de delete não exija um corpo de resposta.
