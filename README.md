# Django REST Framework Recipes API

Este projeto implementa uma API RESTful para um sistema de gerenciamento de receitas, construída utilizando Django REST Framework. A API oferece operações completas de CRUD para receitas e tags, além de diversas funcionalidades adicionais para garantir uma experiência robusta e eficiente.

## Funcionalidades

- **CRUD Completo:** Crie, leia, atualize e exclua receitas e tags com facilidade.
- **Paginação Eficiente:** Navegue através de grandes conjuntos de dados de forma rápida e organizada.
- **Validações Personalizadas:** Garanta a integridade dos dados com validações específicas para receitas.
- **Manipulação de Imagens:** Redimensionamento automático de imagens para garantir uniformidade.
- **Relacionamento entre Modelos:** Relacione receitas com categorias e tags, oferecendo uma estrutura organizada e flexível.

## Endpoints Principais

- **Receitas:**
  - `GET /recipes/` - Lista todas as receitas publicadas.
  - `POST /recipes/` - Cria uma nova receita.
  - `GET /recipes/{id}/` - Recupera detalhes de uma receita específica.
  - `PATCH /recipes/{id}/` - Atualiza parcialmente uma receita.
  - `DELETE /recipes/{id}/` - Exclui uma receita.

- **Tags:**
  - `GET /tags/` - Lista todas as tags.
  - `DELETE /tags/{id}/` - Exclui uma tag específica.

## Tecnologias Utilizadas

- **Django**
- **Django REST Framework**

## Como Usar

## Instalação

Siga estas etapas para configurar o projeto localmente:

1. **Clone o repositório**

    ```bash
    git clone https://github.com/usuario/nome-do-repositorio.git
    ```

2. **Navegue até o diretório do projeto**

    ```bash
    cd nome-do-repositorio
    ```

3. **Crie e ative um ambiente virtual**

    Para Windows:
    
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
    
    Para macOS e Linux:
    
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

4. **Instale as dependências**

    ```bash
    pip install -r requirements.txt
    ```

5. **Configure as variáveis de ambiente**

    - **Instale o `python-dotenv`** se ele não tiver sido instalado do arquivo `requirements.txt`, para gerenciar variáveis de ambiente a partir de um arquivo `.env`:

      ```bash
      pip install python-dotenv
      ```

    - **Crie um arquivo `.env` na raiz do projeto e adicione as seguintes variáveis** (ajuste os valores conforme necessário):

      ```dotenv
      DEBUG=True
      SECRET_KEY=sua_chave_secreta
      DATABASE_URL=postgres://usuario:senha@localhost:5432/nome_do_banco
      ```

    - **Certifique-se de que o arquivo `.env` está listado no `.gitignore`** para não ser commitado no repositório.

      Exemplo de entrada no `.gitignore`:
      ```gitignore
      .env
      ```

    - **Para carregar variáveis do `.env` em seu projeto Django**, adicione o seguinte código no início do seu `settings.py`:

      ```python
      from dotenv import load_dotenv
      import os

      load_dotenv()

      SECRET_KEY = str(os.getenv('SECRET_KEY'))
      DEBUG = str(os.getenv('DEBUG'))
      ```

6. **Gerar uma Nova `SECRET_KEY`**

    Para gerar uma nova `SECRET_KEY`, execute o seguinte comando no terminal:

    ```bash
    python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
    ```

    Copie a saída e adicione ao arquivo `.env` como o valor para `SECRET_KEY`.

7. **Execute as migrações do banco de dados**

    ```bash
    python manage.py makemigrations
    ```
    
    ```bash
    python manage.py migrate
    ```

8. **Crie um superusuário (opcional, para acessar o painel de administração)**

    ```bash
    python manage.py createsuperuser
    ```

9. **Inicie o servidor de desenvolvimento**

    ```bash
    python manage.py runserver
    ```

    O projeto da API estará disponível em `http://127.0.0.1:8000/recipes/api/v2/`

    O projeto de templates estará disponível em `http://127.0.0.1:8000/`.
    
