Write-Output "Instalando dependências..."
python3 -m ensurepip --upgrade
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

Write-Output "Coletando arquivos estáticos..."
python3 manage.py collectstatic --no-input

Write-Output "Aplicando migrações..."
python3 manage.py migrate

Write-Output "Build concluído com sucesso."
