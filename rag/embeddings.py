from langchain_huggingface import HuggingFaceEmbeddings
from settings import EMBEDDING_MODEL

def load_embeddings():
    #return HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        #model_kwargs={"device": "cuda" if torch.cuda.is_available() else "cpu"},
        encode_kwargs={"normalize_embeddings": True}
)