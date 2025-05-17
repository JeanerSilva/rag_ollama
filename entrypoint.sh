#!/bin/sh

echo "⏳ Aguardando daemon do Ollama..."

# Aguarda o Ollama subir antes de executar o modelo
until curl -s http://localhost:11434/api/tags > /dev/null; do
  sleep 2
done

echo "🚀 Rodando modelo llama3..."
ollama run llama3
