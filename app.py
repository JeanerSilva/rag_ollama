import os
import streamlit as st
from config import DOCS_PATH
from rag.vectorstore import load_vectorstore, create_vectorstore
from rag.qa_chain import build_qa_chain
from rag.utils import save_uploaded_files, load_indexed_files
from settings import RETRIEVER_TOP_K
#from rag.normalizador import normalize_query


st.set_page_config(page_title="Pergunte ao PPA", page_icon="🧠")
st.title("🧠 Pergunte ao PPA")

# Session state
if "indexed_files" not in st.session_state:
    st.session_state["indexed_files"] = load_indexed_files()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar: upload
st.sidebar.header("📤 Enviar documentos")
uploaded_files = st.sidebar.file_uploader(
    "Arquivos: .pdf, .txt, .docx, .xlsx, .html",
    type=["pdf", "txt", "docx", "xlsx", "html"],
    accept_multiple_files=True,
)
if uploaded_files:
    save_uploaded_files(uploaded_files)
    st.sidebar.success("✅ Arquivos enviados com sucesso.")

# Sidebar: k config
st.sidebar.markdown("⚙️ **Configurações**")
st.session_state["retriever_k"] = st.sidebar.number_input(
    label="Número de trechos a considerar (k)",
    min_value=1,
    max_value=20,
    value=st.session_state.get("retriever_k", RETRIEVER_TOP_K),
    step=1
)

# Sidebar: reindex
if st.sidebar.button("🔁 Reindexar agora"):
    create_vectorstore()

# Sidebar: arquivos indexados
indexed_files = st.session_state.get("indexed_files", [])
if indexed_files:
    st.sidebar.markdown("📂 **Arquivos indexados:**", unsafe_allow_html=True)
    st.sidebar.markdown(
        "<ul style='padding-left:1.2em;'>"
        + "".join(f"<li style='font-size:0.8em;'>{f}</li>" for f in indexed_files)
        + "</ul>", unsafe_allow_html=True
    )
else:
    st.sidebar.info("Nenhum arquivo indexado.")

# Carregamento
vectorstore = load_vectorstore()
qa_chain = build_qa_chain(vectorstore)
if not qa_chain:
    st.warning("⚠️ A chain ainda não está carregada. Verifique a indexação ou se há documentos na pasta.")

# Formulário de pergunta
if qa_chain:
    with st.form("chat-form", clear_on_submit=True):
        user_input = st.text_input("Digite sua pergunta:")
        submitted = st.form_submit_button("Enviar")

    if submitted and user_input:
        #normalized_question = normalize_query(user_input)
        #result = qa_chain(normalized_question)
        result = qa_chain(user_input)
        resposta = result["result"]
        fontes = result["source_documents"]
        st.session_state.chat_history.append(("user", user_input))
        st.session_state.chat_history.append(("bot", resposta))
        st.session_state.last_contexts = fontes

# Chat
for role, msg in st.session_state.chat_history:
    with st.chat_message("user" if role == "user" else "assistant"):
        st.markdown(msg)

# Fontes
if "last_contexts" in st.session_state:
    with st.expander("📚 Trechos usados na resposta"):
        for doc in st.session_state.last_contexts:
            nome = os.path.basename(doc.metadata.get("source", ""))
            st.markdown(f"**Fonte:** `{nome}`")
            st.markdown(doc.page_content.strip())
            st.markdown("---")

# Limpar conversa
if st.button("🧹 Limpar conversa"):
    st.session_state.chat_history = []
    st.session_state.last_contexts = []
    st.rerun()

# Download
if st.session_state.chat_history:
    for role, msg in reversed(st.session_state.chat_history):
        if role == "bot":
            st.download_button("📥 Baixar última resposta", msg, file_name="resposta.txt")
            break
