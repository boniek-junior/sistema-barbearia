from fastapi import FastAPI
from core.database import Base, engine
from api.router import api_router

@app.on_event("startup")
def on_startup() -> None:
    """Cria as tabelas do banco de dados ao iniciar a aplicação."""
    Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Barbearia API",
    description="API para gerenciamento de clientes e agendamentos.",
    version="1.0.0",
)

# Incluindo o roteador da API
app.include_router(api_router)