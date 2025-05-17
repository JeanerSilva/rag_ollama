import streamlit as st
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from rag.prompt import get_custom_prompt
from settings import TEMPERATURE, RETRIEVER_TOP_K

def build_qa_chain(vectorstore):
    if not vectorstore:
        return None

    llm = Ollama(model="llama3.2", temperature=TEMPERATURE)  # ou outro modelo disponível no Ollama

    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(search_type="similarity", k=st.session_state.get("retriever_k", 6)),
        return_source_documents=True,
        chain_type_kwargs={"prompt": get_custom_prompt()}
    )
