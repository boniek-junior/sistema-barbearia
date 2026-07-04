from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from core.config import settings
from core.database import get_db

# Contexto para criptografia de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema de autenticação via Bearer Token, apontando para a rota do login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/usuarios/login")

def hash_senha(senha: str) -> str:
    """Gera um hash seguro para a senha fornecida."""
    return pwd_context.hash(senha)

def verificar_senha(senha: str, hash_senha: str) -> bool:
    """Verifica se a senha fornecida corresponde ao hash."""
    return pwd_context.verify(senha, hash_senha)

def criar_token_acesso(data: dict, expires_delta: timedelta | None = None) -> str:
    """Cria um token JWT de acesso com os dados fornecidos e tempo de expiração."""
    dados_para_codificar = data.copy()
    if expires_delta:
        expira_em = datetime.now(timezone.utc) + expires_delta
    else:
        expira_em = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    dados_para_codificar.update({"exp": expira_em})
    encoded_jwt = jwt.encode(dados_para_codificar, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def obter_usuario_atual(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Dependência que valida o token e retorna o usuário autenticado.
    Usada para proteger rotas que exigem login."""
    from modules.usuarios import repository as usuarios_repository

    credenciais_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credenciais_invalidas
    except JWTError:
        raise credenciais_invalidas

    usuario = usuarios_repository.obter_usuario_por_email(db, email)
    if usuario is None:
        raise credenciais_invalidas
    return usuario