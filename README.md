# Barbearia

API simples em FastAPI para gerenciamento de clientes e agendamentos.

## Estrutura do projeto

- `main.py` - ponto de entrada da aplicação FastAPI.
- `requirements.txt` - dependências do projeto.
- `core/`
  - `config.py` - configuração de conexão com o banco de dados.
  - `database.py` - criação do engine, sessão e base do SQLAlchemy.
- `api/router.py` - roteador principal do FastAPI que registra módulos.
- `modules/`
  - `clientes/` - módulo para gerenciamento de clientes.
  - `agendamentos/` - módulo para agendamento de serviços.

## Pré-requisitos

- Python 3.11+
- `pip`

## Instalação

1. Abra o terminal no diretório do projeto:
   ```powershell
   cd c:\Projetos\Barbearia
   ```

2. Crie e ative o ambiente virtual:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Instale as dependências:
   ```powershell
   pip install -r requirements.txt
   ```

## Execução

Inicie o servidor com:

```powershell
uvicorn main:app --reload
```

A aplicação ficará disponível em `http://127.0.0.1:8000`.

### Em produção

Para executar em produção é recomendado usar `gunicorn` com o worker do Uvicorn:

```bash
gunicorn -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:$PORT --workers 2
```

Adicione `gunicorn` ao `requirements.txt` (já incluso) e considere usar um `Procfile` ou `render.yaml` para a plataforma de deploy.

## Endpoints

- `POST /clientes/` - cria um cliente.
- `GET /clientes/` - lista todos os clientes.
- `GET /clientes/{cliente_id}` - obtém um cliente pelo ID.
- `POST /agendamentos/` - cria um agendamento.
- `GET /agendamentos/` - lista todos os agendamentos.

## Observações

- O banco SQLite `barbearia.db` é criado automaticamente na raiz do projeto.
- O roteamento está modularizado em `api/router.py` para separar clientes e agendamentos.
- Os módulos usam a arquitetura `controller -> service -> repository`.
