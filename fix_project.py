#!/usr/bin/env python
"""Script para corrigir os arquivos do projeto."""

from pathlib import Path

project_root = Path(__file__).parent

# Dicionário de arquivos e conteúdo
files_content = {
    project_root / "modules" / "clientes" / "repository.py": """from sqlalchemy.orm import Session
from .models import Cliente


def criar_cliente(db: Session, nome: str, email: str, telefone: str) -> Cliente:
    \"\"\"Insere um novo cliente no banco de dados.\"\"\"
    cliente = Cliente(nome=nome, email=email, telefone=telefone)
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente


def listar_clientes(db: Session) -> list[Cliente]:
    \"\"\"Retorna todos os clientes cadastrados.\"\"\"
    return db.query(Cliente).all()


def obter_cliente(db: Session, cliente_id: int) -> Cliente | None:
    \"\"\"Busca um cliente pelo ID.\"\"\"
    return db.query(Cliente).filter(Cliente.id == cliente_id).first()
""",
    project_root / "modules" / "clientes" / "service.py": """from sqlalchemy.orm import Session
from . import repository


def criar_cliente(db: Session, nome: str, email: str, telefone: str):
    \"\"\"Cria um cliente e delega a persistência ao repositório.\"\"\"
    return repository.criar_cliente(db, nome, email, telefone)


def listar_clientes(db: Session):
    \"\"\"Retorna a lista de clientes cadastrados.\"\"\"
    return repository.listar_clientes(db)


def obter_cliente(db: Session, cliente_id: int):
    \"\"\"Retorna um cliente pelo ID.\"\"\"
    return repository.obter_cliente(db, cliente_id)
""",
    project_root / "modules" / "agendamentos" / "controller.py": """from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from . import schemas, service

# Roteador para agendamentos
router = APIRouter()

@router.post("/", response_model=schemas.AgendamentoResponse)
def criar_agendamento(
    agendamento: schemas.AgendamentoCreate,
    db: Session = Depends(get_db),
):
    \"\"\"Cria um novo agendamento.\"\"\"
    return service.criar_agendamento(
        db,
        agendamento.cliente_id,
        agendamento.data,
        agendamento.servico,
    )

@router.get("/", response_model=list[schemas.AgendamentoResponse])
def listar_agendamentos(db: Session = Depends(get_db)):
    \"\"\"Retorna todos os agendamentos gerados.\"\"\"
    return service.listar_agendamentos(db)
""",
    project_root / "modules" / "agendamentos" / "schemas.py": """from datetime import datetime
from pydantic import BaseModel


class AgendamentoBase(BaseModel):
    cliente_id: int
    data: datetime
    servico: str


class AgendamentoCreate(AgendamentoBase):
    \"\"\"Dados necessários para criar um agendamento.\"\"\"
    pass


class AgendamentoResponse(AgendamentoBase):
    \"\"\"Estrutura de resposta de agendamento.\"\"\"
    id: int

    class Config:
        orm_mode = True
""",
    project_root / "modules" / "agendamentos" / "models.py": """from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from core.database import Base


class Agendamento(Base):
    __tablename__ = "agendamentos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    data = Column(DateTime, nullable=False)
    servico = Column(String, nullable=False)

    cliente = relationship("Cliente", backref="agendamentos")
""",
    project_root / "modules" / "agendamentos" / "repository.py": """from sqlalchemy.orm import Session
from .models import Agendamento


def criar_agendamento(db: Session, cliente_id: int, data, servico: str) -> Agendamento:
    \"\"\"Insere um novo agendamento no banco de dados.\"\"\"
    agendamento = Agendamento(cliente_id=cliente_id, data=data, servico=servico)
    db.add(agendamento)
    db.commit()
    db.refresh(agendamento)
    return agendamento


def listar_agendamentos(db: Session) -> list[Agendamento]:
    \"\"\"Retorna todos os agendamentos cadastrados.\"\"\"
    return db.query(Agendamento).all()
""",
    project_root / "modules" / "agendamentos" / "service.py": """from sqlalchemy.orm import Session
from . import repository


def criar_agendamento(db: Session, cliente_id: int, data, servico: str):
    \"\"\"Cria um agendamento para um cliente.\"\"\"
    return repository.criar_agendamento(db, cliente_id, data, servico)


def listar_agendamentos(db: Session):
    \"\"\"Retorna a lista de agendamentos cadastrados.\"\"\"
    return repository.listar_agendamentos(db)
""",
}

# Escrever todos os arquivos
for file_path, content in files_content.items():
    file_path.write_text(content, encoding="utf-8")
    print(f"✓ {file_path.relative_to(project_root)}")

print("\nArquivos corrigidos com sucesso!")
