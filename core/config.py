from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    DATABASE_URL: str = f"sqlite:///{BASE_DIR / 'barbearia.db'}"

    HORARIO_ABERTURA: int = 8
    HORARIO_FECHAMENTO: int = 18
    DURACAO_PADRAO: int = 40

    @field_validator("DATABASE_URL")
    @classmethod
    def fix_postgres_url(cls, v: str) -> str:
        if v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql://", 1)
        return v

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore"
    )


settings = Settings()
