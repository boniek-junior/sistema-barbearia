from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from . import schemas, service

# Roteador para as rotas de clientes
router = APIRouter()

@router.post("/", response_model=schemas.ClienteResponse)
def criar_cliente(
    cliente: schemas.ClienteCreate,
    db: Session = Depends(get_db),
):
    """Cria um novo cliente no sistema."""
    return service.criar_cliente(db, cliente.nome, cliente.email, cliente.telefone)

@router.get("/", response_model=list[schemas.ClienteResponse])
def listar_clientes(db: Session = Depends(get_db)):
    """Retorna a lista de clientes cadastrados."""
    return service.listar_clientes(db)

@router.get("/{cliente_id}", response_model=schemas.ClienteResponse)
def obter_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Retorna um cliente pelo ID."""
    cliente = service.obter_cliente(db, cliente_id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente
