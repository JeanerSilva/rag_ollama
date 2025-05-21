# llm_loader.py

import os
from langchain_community.llms import LlamaCpp
from langchain_ollama import OllamaLLM
from settings import TEMPERATURE, LLM_MODEL

def load_llm(modelo_llm: str):
    if modelo_llm == "GGUF (offline)":
        return LlamaCpp(
            model_path="./.models/mistral-7b-instruct-v0.1.Q4_K_M.gguf",
            n_ctx=4096,
            n_batch=64,
            temperature=TEMPERATURE,
            verbose=False
        )
    else:
        base_url = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        return OllamaLLM(
            model=LLM_MODEL,
            base_url=base_url,
            temperature=TEMPERATURE
        )
