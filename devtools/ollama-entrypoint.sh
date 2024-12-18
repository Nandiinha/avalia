#!/bin/sh
set -e

# Variável para o nome do modelo
MODEL_NAME="mistral"

apt-get update && apt-get install -y curl

echo "Iniciando o entrypoint para Ollama..."

# Iniciar o servidor Ollama em segundo plano
ollama serve &
SERVER_PID=$!

# Esperar o servidor Ollama estar ativo
echo "Aguardando o servidor Ollama estar ativo..."
for i in $(seq 1 10); do
  if curl -s http://localhost:11434/ > /dev/null; then
    echo "Servidor Ollama está ativo."
    break
  fi
  echo "Tentativa $i: Servidor Ollama ainda não está ativo. Aguardando..."
  sleep 2
done

# Fazer o pull do modelo definido na variável
if ollama pull $MODEL_NAME; then
  echo "Modelo $MODEL_NAME baixado com sucesso."
else
  echo "Modelo $MODEL_NAME já disponível ou erro ao baixar."
fi

# Finalizar o servidor Ollama em segundo plano
kill $SERVER_PID

# Iniciar o servidor Ollama no modo principal
echo "Iniciando o servidor Ollama no modo principal..."
exec ollama serve
