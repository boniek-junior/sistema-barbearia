from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import Base, engine
from api.router import api_router
import multiprocessing
import uvicorn

# Criando a instância do FastAPI
app = FastAPI(
    title="Barbearia API",
    description="API para gerenciamento de clientes e agendamentos.",
    version="1.0.0",
)

# Configuração de CORS para permitir o frontend React se comunicar com a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, trocar pelo domínio do frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluindo o roteador da API
app.include_router(api_router, prefix="/api")

# Evento de inicialização para criar as tabelas do banco de dados
@app.on_event("startup")
def on_startup() -> None:
    """Cria as tabelas do banco de dados ao iniciar a aplicação."""
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    multiprocessing.freeze_support()
    uvicorn.run(app, host="127.0.0.1", port=8000)