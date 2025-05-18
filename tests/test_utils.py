from rag.utils import load_indexed_files, save_indexed_files
import os

def test_save_and_load_indexed_files(tmp_path):
    path = tmp_path / "indexed_files.json"
    test_data = ["file1.pdf", "file2.docx"]

    save_indexed_files(test_data, path=str(path))
    loaded = load_indexed_files(path=str(path))

    assert loaded == test_data
