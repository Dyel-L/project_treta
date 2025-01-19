# Projeto de Gerenciamento de Livros

Este é um projeto de gerenciamento de livros utilizando FastAPI, SQLAlchemy e PostgreSQL. O projeto permite a criação, listagem, atualização e exclusão de livros, além de gerenciar empréstimos de livros.

## Requisitos

- Python 3.8+
- PostgreSQL
- Docker

## Instalação

1. Clone o repositório:

    ```bash
    git clone https://github.com/seu-usuario/seu-repositorio.git
    cd seu-repositorio
    ```

2. Crie e ative um ambiente virtual:

    ```bash
    python -m venv venv
    source venv/bin/activate 
    ```

3. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

4. Configure o banco de dados:

    - Certifique-se de que o PostgreSQL está instalado e em execução.
    - Crie um banco de dados chamado `book_db`.
    - Atualize o arquivo `.env` com as informações de conexão do banco de dados, se necessário.

5. Execute as migrações do banco de dados:

    ```bash
    alembic upgrade head
    ```

## Executando o Projeto

### Usando Docker

1. Construa e inicie os containers Docker:

    ```bash
    docker-compose up --build
    ```

2. Acesse a documentação da API em [http://localhost:8000/docs](http://localhost:8000/docs).

### Usando Uvicorn

1. Inicie o servidor FastAPI:

    ```bash
    uvicorn app.main:app --reload
    ```

2. Acesse a documentação da API em [http://localhost:8000/docs](http://localhost:8000/docs).

## Autenticando Usuário

Para acessar os endpoints protegidos, você precisará criar um usuario e obter um token de acesso. Para isso, envie uma requisição POST para `/users` com o seguinte corpo:

```json
{
  "name": "string",
  "password": "string",
  "email": "user@example.com"
}
```
Depois, faça uma requisição POST para `/token` com o email criado e senha, com o token voce pode acessar os endpoints protegidos.

## Endpoints Principais

- **Autenticação**
  - `POST /token`: Autenticação de usuário e obtenção de token.
  - `GET /me`: Obter informações do usuário autenticado.

- **Livros**
  - `GET /books`: Listar todos os livros.
  - `POST /books`: Criar um novo livro.
  - `GET /books/{book_id}`: Obter detalhes de um livro específico.
  - `PUT /books/{book_id}`: Atualizar um livro.
  - `DELETE /books/{book_id}`: Excluir um livro.
  - `PATCH /books/{book_id}/availability`: Alternar a disponibilidade de um livro.

- **Empréstimos**
  - `POST /loans`: Criar um novo empréstimo.
  - `GET /loans`: Listar todos os empréstimos.
  - `GET /loans/{loan_id}`: Obter detalhes de um empréstimo específico.
  - `PUT /loans/{loan_id}`: Atualizar um empréstimo.
  - `DELETE /loans/{loan_id}`: Excluir um empréstimo.

## Estrutura do Projeto

- `app/`: Diretório principal do projeto.
  - `api/`: Contém os roteadores da API.
  - `core/`: Contém a lógica de segurança e configuração.
  - `db/`: Contém os modelos e a configuração do banco de dados.
  - `schemas/`: Contém os esquemas Pydantic.
  - `services/`: Contém a lógica de negócios.
  - `main.py`: Ponto de entrada da aplicação.
