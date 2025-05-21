# qa_chain.py

from langchain.chains import RetrievalQA
from rag.prompt import get_custom_prompt
from settings import RETRIEVER_TOP_K

def build_qa_chain(vectorstore, llm, prompt_template):
    from rag.prompt import get_custom_prompt
    from settings import RETRIEVER_TOP_K

    if not vectorstore or not llm:
        return None

    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(search_type="mmr", k=RETRIEVER_TOP_K, fetch_k=30),
        return_source_documents=True,
        chain_type_kwargs={"prompt": get_custom_prompt(prompt_template)}
    )
