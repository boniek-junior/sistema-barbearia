from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import Base, engine
from api.router import api_router
import os
import sys
import multiprocessing
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

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

# Configuração para servir o Frontend Estático
if hasattr(sys, '_MEIPASS'):
    # Executando no PyInstaller bundle
    base_path = sys._MEIPASS
else:
    # Executando no ambiente normal
    base_path = os.path.dirname(__file__)

frontend_path = os.path.join(base_path, "static")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")

    @app.exception_handler(404)
    async def fallback_to_index(request, exc):
        # Se a rota não for /api/... e o arquivo não for encontrado, envia o index.html (SPA)
        if not request.url.path.startswith("/api/"):
            index_path = os.path.join(frontend_path, "index.html")
            if os.path.exists(index_path):
                return FileResponse(index_path)
        return FileResponse(os.path.join(frontend_path, "404.html")) if os.path.exists(os.path.join(frontend_path, "404.html")) else exc

if __name__ == "__main__":
    multiprocessing.freeze_support()
    uvicorn.run(app, host="127.0.0.1", port=8000)