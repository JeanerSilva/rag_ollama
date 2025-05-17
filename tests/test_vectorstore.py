import pytest
from unittest.mock import patch, MagicMock
from rag.vectorstore import create_vectorstore

@patch("rag.vectorstore.glob.glob", return_value=["test.txt"])
@patch("rag.vectorstore.TextLoader")
@patch("rag.vectorstore.FAISS")
@patch("rag.vectorstore.load_embeddings")
def test_create_vectorstore_success(mock_embeddings, mock_faiss, mock_loader, mock_glob):
    loader_instance = MagicMock()
    loader_instance.load.return_value = [{"page_content": "conteúdo de teste"}]
    mock_loader.return_value = loader_instance

    db_mock = MagicMock()
    mock_faiss.from_documents.return_value = db_mock

    db = create_vectorstore()

    assert db is not None
    mock_faiss.from_documents.assert_called()
