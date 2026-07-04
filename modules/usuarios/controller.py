from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import obter_usuario_atual
from . import schemas, service

# Roteador para as rotas de usuários
router = APIRouter()

# Rota para registrar um novo usuário
@router.post("/registrar", response_model=schemas.UsuarioResponse)
def registrar_usuario(
    usuario: schemas.UsuarioCreate,
    db: Session = Depends(get_db),
):
    """Cria um novo usuário no sistema."""
    return service.registrar_usuario(db, usuario.nome, usuario.email, usuario.senha)

# Rota de login — recebe usuário/senha via formulário e retorna o token
@router.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """Autentica o usuário e retorna um token de acesso."""
    token = service.autenticar_usuario(db, form_data.username, form_data.password)
    return schemas.Token(access_token=token)

# Rota para obter  os dados do usuário logado
@router.get("/me", response_model=schemas.UsuarioResponse)
def obter_usuario_logado(usuario=Depends(obter_usuario_atual)):
    """Retorna os dados do usuário atualmente autenticado."""
    return usuario
