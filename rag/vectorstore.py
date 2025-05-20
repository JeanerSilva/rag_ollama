import os
import glob
import streamlit as st
from config import DOCS_PATH, VECTORDB_PATH
from langchain_community.vectorstores import FAISS
#from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    TextLoader, PyPDFLoader, UnstructuredWordDocumentLoader,
    UnstructuredExcelLoader, UnstructuredHTMLLoader
)
from rag.embeddings import load_embeddings
from rag.utils import save_indexed_files
from langchain.text_splitter import TokenTextSplitter
from transformers import AutoTokenizer




from settings import EMBEDDING_MODEL, CHUNK_OVERLAP, CHUNK_SIZE

def create_vectorstore():
    sidebar_status = st.sidebar.empty()
    sidebar_progress = st.sidebar.progress(0)

    sidebar_status.info("🔄 Reindexando documentos...")
    docs = []
    files = sorted(glob.glob(f"{DOCS_PATH}/*"))
    total = len(files)

    for i, file in enumerate(files):
        ext = os.path.splitext(file)[1].lower()
        filename = os.path.basename(file)
        sidebar_status.markdown(f"📄 Processando: `{filename}`")

        try:
            if ext == ".pdf":
                loader = PyPDFLoader(file)
            elif ext == ".txt":
                loader = TextLoader(file)
            elif ext == ".docx":
                loader = UnstructuredWordDocumentLoader(file)
            elif ext == ".xlsx":
                loader = UnstructuredExcelLoader(file)
            elif ext == ".html":
                loader = UnstructuredHTMLLoader(file)
            else:
                continue
            docs.extend(loader.load())
        except Exception as e:
            st.sidebar.warning(f"⚠️ Erro ao processar `{filename}`: {e}")

        sidebar_progress.progress((i + 1) / total)

    if not docs:
        sidebar_status.error("❌ Nenhum documento válido.")
        sidebar_progress.empty()
        st.stop()

    sidebar_status.markdown(f"📄 Fazendo o splitting com modelo {EMBEDDING_MODEL}...")

    tokenizer = AutoTokenizer.from_pretrained(EMBEDDING_MODEL)

    # Splitter baseado em tokens reais
    splitter = TokenTextSplitter.from_huggingface_tokenizer(
        tokenizer=tokenizer,
        chunk_size=600,
        chunk_overlap=100,
        
        #separators=[
        #"\n\n",  # parágrafos
        #"\n",    # quebras de linha
        #".",     # frases
        #";",     # sentenças curtas
        #",",     # frases compostas
        #" ",     # fallback: palavras
        #""       # fallback final: caractere por caractere
        #]
    )

    sidebar_status.markdown(f"📦 Gerando embeddings. Chunk_size {CHUNK_SIZE} e chunk_overlap {CHUNK_OVERLAP}...")
    # Carregamento e divisão dos documentos
    chunks = splitter.split_documents(docs)

    # Prefixar "passage: " para compatibilidade com E5
    for chunk in chunks:
        chunk.page_content = f"passage: {chunk.page_content.strip()}"

    db = FAISS.from_documents(chunks, load_embeddings())
    db.save_local(VECTORDB_PATH)

    indexed_files = [os.path.basename(f) for f in files]
    st.session_state["indexed_files"] = indexed_files
    save_indexed_files(indexed_files)

    sidebar_status.markdown(f"✅ Documentos indexados com sucesso!")
    sidebar_progress.empty()
    return db

def load_vectorstore():
    if not os.path.exists(os.path.join(VECTORDB_PATH, "index.faiss")):
        return None
    return FAISS.load_local(VECTORDB_PATH, load_embeddings(), allow_dangerous_deserialization=True)
