# Use uma imagem base do Python
FROM python:3.9-slim

# Configurar o diretório de trabalho
WORKDIR /app

# Copiar apenas o arquivo de dependências primeiro
COPY requirements.txt /app/

# Configurar um diretório temporário para cache do pip
ENV PIP_CACHE_DIR=/tmp/pip_cache

# Instalar dependências
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    wget \
    curl \
    libssl-dev \
    libffi-dev \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Instalar o Ollama
RUN curl -O https://ollama.com/download/linux/ollama-cli-latest.tar.gz && \
    tar -xvzf ollama-cli-latest.tar.gz && \
    mv ollama /usr/local/bin/ollama && \
    rm ollama-cli-latest.tar.gz

# Verificar instalação do Ollama
RUN ollama version

# Instalar o modelo Mistral no Ollama
RUN ollama pull mistral

# Instalar o pip e as dependências do projeto usando o cache temporário
RUN pip install --cache-dir=${PIP_CACHE_DIR} --upgrade pip
RUN pip install --cache-dir=${PIP_CACHE_DIR} -r requirements.txt

# Copiar o resto do código do projeto
COPY . /app/

# Coletar arquivos estáticos
RUN python manage.py collectstatic --noinput

# Expor a porta padrão
EXPOSE 8000

# Iniciar o servidor Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "TCC.wsgi:application"]
