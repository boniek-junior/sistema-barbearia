from fastapi import FastAPI
from core.database import Base, engine
from api.router import api_router
from contextlib import asynccontextmanager

# Criando a instância do FastAPI
app = FastAPI(
    title="Barbearia API",
    description="API para gerenciamento de clientes e agendamentos.",
    version="1.0.0",
)

# Incluindo o roteador da API
app.include_router(api_router)

# Evento de inicialização para criar as tabelas do banco de dados
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código a ser executado ao iniciar a aplicação
    Base.metadata.create_all(bind=engine)
    yield
    # Código a ser executado ao encerrar a aplicação

app = FastAPI(lifespan=lifespan)