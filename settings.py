# settings.py

RETRIEVER_TOP_K = 10
CHUNK_SIZE = 600
CHUNK_OVERLAP = 100
TEMPERATURE = 0.7

# Modelos disponíveis
EMBEDDING_OPTIONS = {
    "E5 (multilingual)": "intfloat/multilingual-e5-large",
    "BGE (small EN)": "BAAI/bge-small-en-v1.5"
}

LLM_MODEL = "llama3.2"
