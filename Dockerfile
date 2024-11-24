# Use uma imagem base do Python
FROM python:3.9-slim

# Configurar o diretório de trabalho
WORKDIR /app

# Copiar apenas o arquivo de dependências primeiro
COPY requirements.txt /app/

# Instalar dependências
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o resto do código do projeto
COPY . /app/

# Coletar arquivos estáticos
RUN python manage.py collectstatic --noinput

# Expor a porta padrão
EXPOSE 8000

# Iniciar o servidor Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "TCC.wsgi:application"]
