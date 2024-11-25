# Executando o Projeto Localmente

Se preferir configurar o ambiente localmente sem usar Docker, siga este guia.

## Pré-requisitos

Certifique-se de ter os seguintes softwares instalados em sua máquina:

- **Python 3.9.\***
- **pip** (gerenciador de pacotes Python)
- **virtualenv** (opcional, mas recomendado)

## Passo a Passo

1. **Clone o Repositório:**
   ```bash
   git clone https://github.com/Nandiinha/avalia.git
   cd avalia
   ```

2. **Crie e Ative um Ambiente Virtual:**
   - **Linux/Mac:**
     ```bash
     python -m venv venv
     source venv/bin/activate
     ```
   - **Windows:**
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

3. **Instale as Dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o Arquivo `.env`:**
   - **Linux/Mac:**  
     Use o comando:
     ```bash
     cp .env.local .env
     ```
   - **Windows:**  
     Execute este comando no terminal PowerShell:
        ```powershell
        copy .env.local .env
        ```

5. **Execute as Migrações do Banco de Dados:**
   ```bash
   python manage.py migrate
   ```

6. **Inicie o Servidor de Desenvolvimento:**
   ```bash
   python manage.py runserver
   ```

   Acesse o projeto em [http://127.0.0.1:8000](http://127.0.0.1:8000).