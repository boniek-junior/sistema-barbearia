from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import obter_usuario_atual
from . import schemas, service

router = APIRouter()

@router.post("/", response_model=schemas.ClienteResponse)
def criar_cliente(
    cliente: schemas.ClienteCreate,
    db: Session = Depends(get_db),
    usuario=Depends(obter_usuario_atual),
):
    """Cria um novo cliente vinculado ao usuario logado."""
    return service.criar_cliente(db, cliente.nome, cliente.telefone, usuario.id)

@router.get("/", response_model=list[schemas.ClienteResponse])
def listar_clientes(db: Session = Depends(get_db), usuario=Depends(obter_usuario_atual)):
    """Retorna a lista de clientes do usuario logado."""
    return service.listar_clientes(db, usuario.id)

@router.get("/{cliente_id}", response_model=schemas.ClienteResponse)
def obter_cliente(cliente_id: int, db: Session = Depends(get_db), usuario=Depends(obter_usuario_atual)):
    """Retorna um cliente do usuario logado pelo ID."""
    cliente = service.obter_cliente(db, cliente_id, usuario.id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente nao encontrado")
    return cliente

@router.put("/{cliente_id}", response_model=schemas.ClienteResponse)
def atualizar_cliente(
    cliente_id: int,
    dados: schemas.ClienteUpdate,
    db: Session = Depends(get_db),
    usuario=Depends(obter_usuario_atual),
):
    """Atualiza os dados de um cliente existente do usuario logado."""
    cliente_atualizado = service.atualizar_cliente(db, cliente_id, dados.dict(exclude_unset=True), usuario.id)
    if cliente_atualizado is None:
        raise HTTPException(status_code=404, detail="Cliente nao encontrado")
    return cliente_atualizado

@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(obter_usuario_atual),
):
    """Deleta um cliente do usuario logado."""
    return service.deletar_cliente(db, cliente_id, usuario.id)
