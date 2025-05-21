# app.py

import os
import time
import streamlit as st
from config import DOCS_PATH
from settings import RETRIEVER_TOP_K, EMBEDDING_OPTIONS

from rag.vectorstore import load_vectorstore, create_vectorstore
from rag.qa_chain import build_qa_chain
from rag.utils import save_uploaded_files, load_indexed_files
from rag.llm_loader import load_llm
from rag.chat_history import generate_session_id, save_chat

from rag.prompt import get_saved_prompt, save_prompt, DEFAULT_PROMPT_TEMPLATE   

# Configurações da interface
st.set_page_config(page_title="Pergunte ao PPA", page_icon="🧠")
st.title("🧠 Pergunte ao PPA")

# Estado inicial
if "indexed_files" not in st.session_state:
    st.session_state["indexed_files"] = load_indexed_files()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "chat_session_id" not in st.session_state:
    st.session_state.chat_session_id = generate_session_id()

# Prompt personalizado
st.subheader("🛠️ Prompt personalizado")

if "prompt_template" not in st.session_state:
    st.session_state["prompt_template"] = get_saved_prompt()

edited_prompt = st.text_area(
    "Edite o template do prompt abaixo (use {context} e {question}):",
    value=st.session_state["prompt_template"],
    height=400,
    key="prompt_editor"
)

if st.button("💾 Salvar prompt"):
    save_prompt(edited_prompt)
    st.session_state["prompt_template"] = edited_prompt
    st.success("Prompt salvo com sucesso!")

# Sidebar: Configurações
st.sidebar.markdown("⚙️ **Configurações**")

st.session_state["retriever_k"] = st.sidebar.number_input(
    label="Número de trechos a considerar (k)",
    min_value=1,
    max_value=20,
    value=st.session_state.get("retriever_k", RETRIEVER_TOP_K),
    step=1
)

# Sidebar: LLM
st.sidebar.markdown("🧠 **Modelo de linguagem**")
modelo_llm = st.sidebar.radio(
    "Modo de execução:",
    ["GGUF (offline)", "Ollama (servidor)", "OpenAI (API)"]
)

st.session_state["modelo_llm"] = modelo_llm

# Sidebar: Embedding
st.sidebar.markdown("🧬 **Modelo de embedding**")
embed_model_label = st.sidebar.selectbox("Escolha o modelo:", list(EMBEDDING_OPTIONS.keys()))
embed_model_name = EMBEDDING_OPTIONS[embed_model_label]
st.session_state["embedding_model"] = embed_model_name

# Sidebar: Reindexar
if st.sidebar.button("🔁 Reindexar agora"):
    create_vectorstore(embed_model_name)

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

# Sidebar: Upload
st.sidebar.header("📤 Enviar documentos")
uploaded_files = st.sidebar.file_uploader(
    "Arquivos: .pdf, .txt, .docx, .xlsx, .html",
    type=["pdf", "txt", "docx", "xlsx", "html"],
    accept_multiple_files=True,
)
if uploaded_files:
    save_uploaded_files(uploaded_files)
    st.sidebar.success("✅ Arquivos enviados com sucesso.")

# Carregar index e LLM
vectorstore = load_vectorstore(embed_model_name)
if not vectorstore:
    st.warning("⚠️ Nenhum índice encontrado para esse modelo. Reindexe primeiro.")
    st.stop()

llm = load_llm(modelo_llm)
qa_chain = build_qa_chain(vectorstore, llm, st.session_state["prompt_template"])
if not qa_chain:
    st.warning("⚠️ A chain não está carregada.")
    st.stop()

# Formulário de pergunta
with st.form("chat-form", clear_on_submit=True):
    user_input = st.text_input(
        "Digite sua pergunta:",
        value="Quais são os Objetivos Específicos do Programa Abastecimento e Soberania Alimentar"
    )
    submitted = st.form_submit_button("Enviar")

if submitted and user_input:
    query = f"query: {user_input}"
    start = time.time()
    result = qa_chain.invoke({"query": query})
    elapsed = time.time() - start

    resposta = result["result"]
    fontes = result["source_documents"]

    st.session_state.chat_history.append(("user", user_input))
    st.session_state.chat_history.append(("bot", resposta))
    st.session_state.last_contexts = fontes

    # Salvar histórico por sessão
    save_chat(st.session_state.chat_session_id, st.session_state.chat_history)

    # Exibir tempo
    st.sidebar.success(f"⏱️ Resposta em {elapsed:.2f} segundos")

    # Mostrar chunks retornados
    with st.expander("🔬 Depuração: Chunks retornados pelo retriever"):
        for doc in fontes:
            st.markdown(doc.page_content)

# Exibição estilo chat
for role, msg in st.session_state.chat_history:
    with st.chat_message("user" if role == "user" else "assistant"):
        st.markdown(msg)

# Fontes da resposta
if "last_contexts" in st.session_state:
    with st.expander("📚 Trechos usados na resposta"):
        for doc in st.session_state.last_contexts:
            source = doc.metadata.get("source", "desconhecido")
            nome = os.path.basename(source)
            tipo = os.path.splitext(nome)[1].replace(".", "").upper()
            st.markdown(f"**Fonte:** `{nome}` ({tipo})")
            st.markdown(doc.page_content.strip())
            st.markdown("---")

# Limpar conversa
if st.button("🧹 Limpar conversa"):
    st.session_state.chat_history = []
    st.session_state.last_contexts = []
    st.rerun()

# Download da resposta
if st.session_state.chat_history:
    for role, msg in reversed(st.session_state.chat_history):
        if role == "bot":
            st.download_button("📥 Baixar última resposta", msg, file_name="resposta.txt")
            break

