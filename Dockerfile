FROM python:3.10-slim

# Instalar dependências de sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Criar diretório da aplicação
WORKDIR /app

# Copiar arquivos
COPY . .

# Instalar dependências Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expor porta do Streamlit
EXPOSE 8501

# Comando para iniciar o app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
