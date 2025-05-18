from rag.qa_chain import build_qa_chain
from rag.vectorstore import create_vectorstore
import os

def test_build_qa_chain(tmp_path):
    os.makedirs(tmp_path / "docs", exist_ok=True)
    with open(tmp_path / "docs" / "test.txt", "w") as f:
        f.write("Jeaner é feliz.")

    db = create_vectorstore(str(tmp_path / "docs"), str(tmp_path / "vectordb"))
    chain = build_qa_chain(db)
    assert chain is not None
    assert hasattr(chain, "run")
