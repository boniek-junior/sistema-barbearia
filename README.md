# Sistema de Barbearia

Sistema completo para gerenciamento de clientes e agendamentos de uma barbearia, composto por API backend em FastAPI (Python) e frontend em Next.js (React/TypeScript).

## Estrutura do Projeto

### Backend (sistema-barbearia/)
- `main.py` - Ponto de entrada da aplicação FastAPI.
- `requirements.txt` - Dependências Python.
- `core/`
  - `config.py` - Configuração de conexão com o banco de dados.
  - `database.py` - Criação do engine, sessão e base do SQLAlchemy.
- `api/router.py` - Roteador principal do FastAPI que registra módulos.
- `modules/`
  - `clientes/` - Módulo para gerenciamento de clientes.
  - `agendamentos/` - Módulo para agendamento de serviços.

### Frontend (frontend-sistema-barbearia/)
- Aplicação Next.js com TypeScript, Tailwind CSS e componentes shadcn/ui.
- Interface responsiva para desktop e mobile.

## Pré-requisitos

- **Python 3.11+** (para o backend)
- **Node.js 18+** (para o frontend)
- **Git** (para clonar repositórios)

## Instalação e Configuração

### 1. Clonagem dos Repositórios

```bash
# Clonar o repositório principal (backend)
git clone https://github.com/seu-usuario/sistema-barbearia.git
cd sistema-barbearia

# Clonar o frontend (se não estiver incluído)
git clone https://github.com/boniek-junior/frontend-sistema-barbearia.git ../frontend-sistema-barbearia
```

### 2. Configuração do Backend

1. Navegue até o diretório do backend:
   ```bash
   cd sistema-barbearia
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv .venv
   # Windows
   .\.venv\Scripts\Activate.ps1
   # Linux/Mac
   source .venv/bin/activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Configuração do Frontend

1. Navegue até o diretório do frontend:
   ```bash
   cd ../frontend-sistema-barbearia
   ```

2. Instale as dependências:
   ```bash
   npm install
   # ou se usar pnpm
   pnpm install
   ```

## Execução

### Backend

1. No diretório `sistema-barbearia`, execute:
   ```bash
   uvicorn main:app --reload
   ```

2. O backend estará disponível em: `http://127.0.0.1:8000`
3. Documentação da API: `http://127.0.0.1:8000/docs` (Swagger UI)

### Frontend

1. No diretório `frontend-sistema-barbearia`, execute:
   ```bash
   npm run dev
   # ou
   pnpm dev
   ```

2. O frontend estará disponível em: `http://localhost:3000`

### Executando Ambos Simultaneamente

Abra dois terminais separados:

**Terminal 1 (Backend):**
```bash
cd sistema-barbearia
uvicorn main:app --reload
```

**Terminal 2 (Frontend):**
```bash
cd frontend-sistema-barbearia
npm run dev
```

## Funcionalidades

### Backend
- **Clientes**: CRUD completo (criar, listar, atualizar, deletar)
- **Agendamentos**: Criar agendamentos com validações de horário e conflitos
- **Banco de Dados**: SQLite (criado automaticamente)
- **Validações**: Nomes completos, telefones únicos, horários de funcionamento (8h-18h)

### Frontend
- Dashboard com estatísticas
- Gerenciamento de clientes
- Sistema de agendamentos
- Interface responsiva
- Integração completa com a API

## Endpoints da API

### Clientes
- `POST /clientes/` - Criar novo cliente
  - Body: `{"nome": "João Silva", "telefone": "11999999999"}`
- `GET /clientes/` - Listar todos os clientes
- `GET /clientes/{id}` - Obter cliente específico
- `PUT /clientes/{id}` - Atualizar cliente
- `DELETE /clientes/{id}` - Deletar cliente

### Agendamentos
- `POST /agendamentos/` - Criar novo agendamento
  - Body: `{"cliente_id": 1, "inicio": "2026-05-09T14:00:00", "servico": "corte"}`
- `GET /agendamentos/` - Listar agendamentos (opcional: `?data=2026-05-09`)
- `GET /agendamentos/{id}` - Obter agendamento específico
- `PATCH /agendamentos/{id}/status` - Atualizar status do agendamento
  - Body: `{"status": "confirmado"}`

## Validações

### Clientes
- Nome deve conter pelo menos nome e sobrenome
- Telefone deve ter apenas dígitos e no mínimo 8 caracteres
- Telefone deve ser único no sistema

### Agendamentos
- Horário deve estar entre 08:00 e 18:00
- Não pode agendar para datas/horários passados
- Não pode haver conflitos de horário
- Cliente deve existir
- Serviço deve ser válido

## Desenvolvimento

Para contribuir com o projeto:

1. Faça um fork do repositório
2. Crie uma branch para sua feature: `git checkout -b feature/nova-funcionalidade`
3. Faça suas alterações e commits
4. Push para sua branch: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

- `POST /clientes/` - cria um cliente.
- `GET /clientes/` - lista todos os clientes.
- `GET /clientes/{cliente_id}` - obtém um cliente pelo ID.
- `POST /agendamentos/` - cria um agendamento.
- `GET /agendamentos/` - lista todos os agendamentos.

## Observações

- O banco SQLite `barbearia.db` é criado automaticamente na raiz do projeto.
- O roteamento está modularizado em `api/router.py` para separar clientes e agendamentos.
- Os módulos usam a arquitetura `controller -> service -> repository`.
