# Nome da aplicação e variáveis globais
APP_NAME = avalia-app
DOCKER_IMAGE = $(APP_NAME):latest
DOCKER_PORT = 8000
CONTAINER_PORT = 8000
ENV_FILE = .env

# Caminho para o diretório do projeto
APP_DIR = $(shell pwd)

# Hash do commit atual do Git
GIT_COMMIT = $(shell git rev-parse --short HEAD)

# Alvo padrão (ajuda)
.PHONY: help
help:
	@echo "Comandos disponíveis:"
	@echo "  Comandos do App:"
	@echo "    make django-migrate    - Executar as migrações do banco de dados"
	@echo "    make launch            - Abrir o shell do Django no container"
	@echo "  Comandos do Docker:"
	@echo "    make docker-build      - Compilar a imagem Docker"
	@echo "    make docker-up         - Subir o container Docker"
	@echo "    make docker-down       - Parar e remover containers"
	@echo "    make logs       - Ver os logs do container em execução"
	@echo "    make deploy     - Fazer deploy da aplicação com tag baseada no commit"

# ============================
# Logs das Configurações
# ============================

# Logar as configurações do ambiente
.PHONY: log-config
log-config:
	@echo "================ Configurações ================="
	@echo "Nome da aplicação: $(APP_NAME)"
	@echo "Imagem Docker: $(DOCKER_IMAGE)"
	@echo "Porta do Docker: $(DOCKER_PORT)"
	@echo "Porta do Container: $(CONTAINER_PORT)"
	@echo "Arquivo de Ambiente: $(ENV_FILE)"
	@echo "Diretório do Projeto: $(APP_DIR)"
	@echo "Commit Git Atual: $(GIT_COMMIT)"
	@echo "================================================"

# ============================
# Comandos do App
# ============================

# Executar migrações no banco de dados
.PHONY: django-migrate
django-migrate: log-config
	@echo "Executando migrações do banco de dados..."
	docker exec $(APP_NAME) python manage.py migrate

# Abrir o shell do Django no container
.PHONY: launch
launch: log-config
	@echo "Abrindo o shell do Django..."
	docker exec -it $(APP_NAME) python manage.py shell

# ============================
# Comandos do Docker
# ============================

# Compilar a imagem Docker
.PHONY: docker-build
docker-build: log-config
	@echo "Construindo a imagem Docker..."
	docker build --build-arg GIT_COMMIT_HASH=$(GIT_COMMIT) -t $(DOCKER_IMAGE) .

# Subir o container Docker
.PHONY: docker-up
docker-up: log-config
	@echo "Iniciando o container Docker..."
	docker run -d --name $(APP_NAME) -p $(DOCKER_PORT):$(CONTAINER_PORT) --env-file $(ENV_FILE) $(DOCKER_IMAGE)

# Parar e remover containers
.PHONY: docker-down
docker-down: log-config
	@echo "Parando e removendo containers..."
	docker stop $(APP_NAME) || true
	docker rm $(APP_NAME) || true

# Ver os logs do container em execução
.PHONY: logs
logs: log-config
	@echo "Exibindo logs do container..."
	docker logs -f $(APP_NAME)

# Fazer deploy da aplicação
.PHONY: deploy
deploy: docker-build docker-down docker-up
	@echo "Aplicação implantada com sucesso! Versão: $(GIT_COMMIT)"
