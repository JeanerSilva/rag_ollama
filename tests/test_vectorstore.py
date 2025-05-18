from rag.vectorstore import create_vectorstore
from langchain_community.vectorstores import FAISS
import os

def test_create_vectorstore(tmp_path):
    os.makedirs(tmp_path / "docs", exist_ok=True)
    with open(tmp_path / "docs" / "test.txt", "w") as f:
        f.write("Jeaner é feliz.")

    db = create_vectorstore(str(tmp_path / "docs"), str(tmp_path / "vectordb"))
    assert isinstance(db, FAISS)
