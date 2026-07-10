from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import obter_usuario_atual
from . import schemas, service
import re

# Roteador para as rotas de clientes
router = APIRouter()

# Rota para criar um novo cliente
@router.post("/", response_model=schemas.ClienteResponse)
def criar_cliente(
    cliente: schemas.ClienteCreate,
    db: Session = Depends(get_db),
    usuario=Depends(obter_usuario_atual),
):
    """Cria um novo cliente no sistema."""
    return service.criar_cliente(db, cliente.nome, cliente.telefone)

# Rota para listar todos os clientes
@router.get("/", response_model=list[schemas.ClienteResponse])
def listar_clientes(db: Session = Depends(get_db), usuario=Depends(obter_usuario_atual)):
    """Retorna a lista de clientes cadastrados."""
    return service.listar_clientes(db)

# Rota para obter um cliente pelo ID
@router.get("/{cliente_id}", response_model=schemas.ClienteResponse)
def obter_cliente(cliente_id: int, db: Session = Depends(get_db), usuario=Depends(obter_usuario_atual)):
    """Retorna um cliente pelo ID."""
    cliente = service.obter_cliente(db, cliente_id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente

# Rota para atualizar um cliente existente
@router.put("/{cliente_id}", response_model=schemas.ClienteResponse)
def atualizar_cliente(
    cliente_id: int,
    dados: schemas.ClienteUpdate,
    db: Session = Depends(get_db),
    usuario=Depends(obter_usuario_atual),
):
    """Atualiza os dados de um cliente existente."""
    cliente_atualizado = service.atualizar_cliente(db, cliente_id, dados.dict(exclude_unset=True))
    if cliente_atualizado is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente_atualizado

# Rota para deletar um cliente
@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(obter_usuario_atual),
):
    """Deleta um cliente do banco de dados."""
    return service.deletar_cliente(db, cliente_id)
