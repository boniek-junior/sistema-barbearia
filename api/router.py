from fastapi import APIRouter
from modules.agendamentos.controller import router as agendamentos_router
from modules.clientes.controller import router as clientes_router

# Criando o roteador principal da API
api_router = APIRouter()

# Incluindo os roteadores dos módulos de clientes.
api_router.include_router(clientes_router, prefix="/clientes", tags=["clientes"])

# Incluindo os roteadores dos módulos de agendamentos.
api_router.include_router(agendamentos_router, prefix="/agendamentos", tags=["agendamentos"])