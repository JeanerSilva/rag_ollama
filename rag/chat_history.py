# rag/chat_history.py

import os
import json
import uuid
from datetime import datetime

CHAT_DIR = "./chat_sessions"
os.makedirs(CHAT_DIR, exist_ok=True)

def generate_session_id():
    return datetime.now().strftime("%Y%m%d_%H%M%S_") + str(uuid.uuid4())[:8]

def save_chat(session_id, history):
    path = os.path.join(CHAT_DIR, f"{session_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def load_chat(session_id):
    path = os.path.join(CHAT_DIR, f"{session_id}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []
