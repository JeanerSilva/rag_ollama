# config.py

import os
from dotenv import load_dotenv

DOCS_PATH = "./docs"
VECTORDB_PATH = "./vectordb"
INDEXED_LIST_PATH = "./indexed/indexed_files.json"

os.makedirs(DOCS_PATH, exist_ok=True)
os.makedirs(VECTORDB_PATH, exist_ok=True)

load_dotenv()
