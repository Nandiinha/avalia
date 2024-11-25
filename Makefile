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
	@echo "    make container-build      - Compilar a imagem Docker"
	@echo "    make container-up - Subir os containers com docker-compose"
	@echo "    make container-down - Parar e remover os containers com docker-compose"
	@echo "    make logs              - Ver os logs do container em execução"
	@echo "    make deploy            - Fazer deploy da aplicação com tag baseada no commit"

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

# Garantir permissões de execução para scripts .sh específicos
.PHONY: fix-permissions
fix-permissions:
	@echo "Garantindo permissões de execução para scripts específicos..."
	chmod +x $(APP_DIR)/devtools/ollama-entrypoint.sh
	chmod +x $(APP_DIR)/devtools/wait-for-it.sh

# Compilar a imagem Docker
.PHONY: container-build
container-build: log-config fix-permissions
	@echo "Construindo a imagem Docker..."
	docker build --build-arg GIT_COMMIT_HASH=$(GIT_COMMIT) -t $(DOCKER_IMAGE) .

# Subir os containers Docker usando docker-compose
.PHONY: container-up
container-up: log-config fix-permissions
	@echo "Subindo os containers com docker-compose..."
	docker-compose up --build -d

# Parar os containers Docker usando docker-compose
.PHONY: container-down
container-down: log-config
	@echo "Parando e removendo os containers com docker-compose..."
	docker-compose down

# Ver os logs do container em execução
.PHONY: logs
logs: log-config
	@echo "Exibindo logs do container..."
	docker logs -f $(APP_NAME)

# Fazer deploy da aplicação
.PHONY: deploy
deploy: container-build container-down container-up logs
	@echo "Aplicação implantada com sucesso! Versão: $(GIT_COMMIT)"
