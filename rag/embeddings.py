#from langchain_huggingface import HuggingFaceEmbeddings

#def load_embeddings():
#    return HuggingFaceEmbeddings(model_name="BAAI/bge-small-pt")

from langchain_huggingface import HuggingFaceEmbeddings
def load_embeddings():
    return HuggingFaceEmbeddings(
        model_name="intfloat/multilingual-e5-small",
        encode_kwargs={"normalize_embeddings": True}  # recomendado
)

#baixar o modelo
#def load_embeddings():
#return HuggingFaceEmbeddings(
#    model_name="./models/bge-small-en-v1.5"
#)
