# embeddings.py

from langchain_huggingface import HuggingFaceEmbeddings

def load_embeddings(model_name: str):
    return HuggingFaceEmbeddings(
        model_name=model_name,
        encode_kwargs={"normalize_embeddings": True}
    )
