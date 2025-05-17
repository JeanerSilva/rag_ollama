from rag.qa_chain import build_qa_chain
from unittest.mock import MagicMock

def test_build_qa_chain_success():
    mock_vectorstore = MagicMock()
    mock_vectorstore.as_retriever.return_value = "mock_retriever"

    chain = build_qa_chain(mock_vectorstore)
    assert chain is not None
    assert hasattr(chain, "run")
