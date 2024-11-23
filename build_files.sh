#!/bin/bash

set -e  # Abortar o script se ocorrer um erro

echo "Instalando dependências..."
python3 -m ensurepip --upgrade
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

echo "Coletando arquivos estáticos..."
python3 manage.py collectstatic --no-input

echo "Aplicando migrações..."
python3 manage.py migrate

echo "Build concluído com sucesso."
