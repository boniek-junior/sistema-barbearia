from sqlalchemy.orm import Session
from .models import Usuario

#Funcao para criar um novo usuário no banco de dados
def criar_usuario(db: Session, usuario: Usuario) -> Usuario:
    """insere um novo usuário no banco de dados."""
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

#Funcao para obter um usuário pelo email
def obter_usuario_por_email(db: Session, email: str) -> Usuario | None:
    """Retorna um usuário pelo email, ou None se não encontrado."""
    return db.query(Usuario).filter(Usuario.email == email).first()