import os
import json
from rag import utils

def test_save_and_load_indexed_files(tmp_path):
    test_file = tmp_path / "indexed.json"
    file_list = ["file1.pdf", "file2.docx"]

    # Override global path
    utils.INDEXED_LIST_PATH = str(test_file)

    utils.save_indexed_files(file_list)
    loaded = utils.load_indexed_files()

    assert loaded == file_list
    assert os.path.exists(test_file)
