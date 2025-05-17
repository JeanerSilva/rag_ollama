from rag.embeddings import load_embeddings

def test_load_embeddings():
    embeddings = load_embeddings()
    assert embeddings is not None
    assert hasattr(embeddings, "embed_query")
