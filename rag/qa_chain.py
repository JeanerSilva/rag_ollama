# qa_chain.py

from langchain.chains import RetrievalQA
from rag.prompt import get_custom_prompt
from settings import RETRIEVER_TOP_K

def build_qa_chain(vectorstore, llm):
    if not vectorstore or not llm:
        return None

    k = RETRIEVER_TOP_K
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(search_type="mmr", k=k, fetch_k=30),
        return_source_documents=True,
        chain_type_kwargs={"prompt": get_custom_prompt()}
    )
