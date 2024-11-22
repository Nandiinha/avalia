# Executando o Projeto com Docker

Este guia explica como configurar e rodar o projeto **Avalia Django App** usando Docker, uma maneira fácil e padronizada de configurar o ambiente de desenvolvimento.

## Pré-requisitos

- **Docker** instalado em sua máquina.
- **Docker Compose** instalado.

## Passo a Passo

1. **Crie o arquivo `.env` com base no exemplo:**
   ```bash
   cp .env.example .env
   ```

2. **Construa e inicie os containers:**
   ```bash
   docker-compose up --build
   ```

3. **Acesse o projeto no navegador:**  
   O projeto estará disponível em [http://localhost:8000](http://localhost:8000).

4. **Parar os containers:**  
   Quando quiser parar o ambiente de desenvolvimento, execute:
   ```bash
   docker-compose down
   ```

5. **Acessar o terminal do container Django (opcional):**  
   Para rodar comandos no container Django, use:
   ```bash
   docker exec -it <container_id> sh
   ```

## Vantagens de Usar Docker

- **Padronização:** Configura o ambiente de maneira consistente em diferentes máquinas.
- **Isolamento:** Evita conflitos com configurações locais.
- **Facilidade:** Menos dependências para configurar manualmente.
