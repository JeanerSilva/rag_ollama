# vectorstore.py
import hashlib
import os, glob, traceback
import streamlit as st
from config import DOCS_PATH
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import (
    TextLoader, PyPDFLoader, UnstructuredWordDocumentLoader,
    UnstructuredExcelLoader, UnstructuredHTMLLoader
)
from rag.embeddings import load_embeddings
from rag.utils import save_indexed_files
from langchain.text_splitter import TokenTextSplitter
from transformers import AutoTokenizer
from settings import CHUNK_OVERLAP, CHUNK_SIZE

def hash_file(filepath):
    with open(filepath, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def get_vectordb_path(model_name):
    safe_name = model_name.split("/")[-1].replace("-", "_")
    path = f"./vectordb_{safe_name}"
    os.makedirs(path, exist_ok=True)
    return path

def create_vectorstore(model_name):
    sidebar_status = st.sidebar.empty()
    sidebar_progress = st.sidebar.progress(0)
    vectordb_path = get_vectordb_path(model_name)

    sidebar_status.info("🔄 Reindexando documentos...")
    docs = []
    files = sorted(glob.glob(f"{DOCS_PATH}/*"))
    total = len(files)
    sucesso = 0
    falha = 0

    for i, file in enumerate(files):
        ext = os.path.splitext(file)[1].lower()
        filename = os.path.basename(file)
        sidebar_progress.markdown(f"📄 Processando: `{filename}`")

        try:
            if ext == ".pdf":
                loader = PyPDFLoader(file)
            elif ext == ".txt":
                loader = TextLoader(file, encoding="utf-8")
            elif ext == ".docx":
                loader = UnstructuredWordDocumentLoader(file)
            elif ext == ".xlsx":
                loader = UnstructuredExcelLoader(file)
            elif ext == ".html":
                loader = UnstructuredHTMLLoader(file)
            else:
                continue
            docs.extend(loader.load())
            sucesso += 1
        except Exception as e:
            falha += 1
            sidebar_progress.markdown(f"⚠️ Erro ao processar `{filename}`: {e}")
            traceback.print_exc()

        sidebar_progress.progress((i + 1) / total)

    sidebar_status.markdown(f"📄 Fazendo o splitting com {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    splitter = TokenTextSplitter.from_huggingface_tokenizer(
        tokenizer=tokenizer,
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    sidebar_status.markdown(f"📦 Gerando embeddings...")
    chunks = splitter.split_documents(docs)
    for chunk in chunks:
        chunk.page_content = f"passage: {chunk.page_content.strip()}"

    embeddings = load_embeddings(model_name)
    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(vectordb_path)

    indexed_files = [f"{os.path.basename(f)} | {hash_file(f)}" for f in files]

    st.session_state["indexed_files"] = indexed_files
    save_indexed_files(indexed_files)

    sidebar_status.markdown(f"✅ Documentos indexados com sucesso!")
    sidebar_progress.empty()
    return db

def load_vectorstore(model_name):
    vectordb_path = get_vectordb_path(model_name)
    index_file = os.path.join(vectordb_path, "index.faiss")
    if not os.path.exists(index_file):
        return None
    embeddings = load_embeddings(model_name)
    return FAISS.load_local(vectordb_path, embeddings, allow_dangerous_deserialization=True)
