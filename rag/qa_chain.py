import os
import streamlit as st
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from rag.prompt import get_custom_prompt
from settings import TEMPERATURE

def build_qa_chain(vectorstore):
    if not vectorstore:
        st.warning("⚠️ Vetor de documentos não carregado.")
        return None

    # Lê o host do Ollama via variável de ambiente (com fallback)
    ollama_base_url = os.getenv("OLLAMA_HOST", "http://localhost:11434")

    # Inicializa a LLM
    try:
        llm = Ollama(
            model="llama3",              # 👈 seu modelo principal
            base_url=ollama_base_url,
            temperature=TEMPERATURE
        )
    except Exception as e:
        st.error(f"❌ Erro ao conectar com o Ollama: {e}")
        return None

    # Define quantos trechos relevantes buscar (k)
    k = st.session_state.get("retriever_k", 6)

    # Cria a cadeia QA com recuperação de fontes
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(search_type="similarity", k=k),
        return_source_documents=True,
        chain_type_kwargs={"prompt": get_custom_prompt()}
    )

    return qa_chain
