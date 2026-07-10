from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from core.security import hash_senha, verificar_senha, criar_token_acesso
from . import repository
from .models import Usuario

# Serviço para registrar um novo usuário
def registrar_usuario(db: Session, nome: str, email: str, senha: str):
    """Registra um novo usuário no sistema."""
    # Verifica se o email já está em uso
    usuario_existente = repository.obter_usuario_por_email(db, email)
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já está em uso"
        )

    # Cria o hash da senha
    senha_hash = hash_senha(senha)

    # Monta o objeto e cria o usuário no banco de dados
    novo_usuario = Usuario(nome=nome, email=email, senha_hash=senha_hash)
    novo_usuario = repository.criar_usuario(db, novo_usuario)

    return novo_usuario

# Serviço para autenticar um usuário e gerar um token JWT
def autenticar_usuario(db: Session, email: str, senha: str):
    """Autentica um usuário e retorna um token JWT se as credenciais forem válidas."""
    usuario = repository.obter_usuario_por_email(db, email)
    if not usuario or not verificar_senha(senha, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Cria o token de acesso
    token_de_acesso = {"sub": usuario.email}
    token = criar_token_acesso(token_de_acesso)

    return token