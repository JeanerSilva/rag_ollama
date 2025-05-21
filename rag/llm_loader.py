# rag/llm_loader.py

import os
from dotenv import load_dotenv
from langchain_community.llms import LlamaCpp
from langchain_ollama import OllamaLLM
from langchain_openai import ChatOpenAI
from settings import TEMPERATURE, LLM_MODEL, OPENAI_MODEL


load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

def load_llm(modelo_llm: str):
    if modelo_llm == "GGUF (offline)":
        return LlamaCpp(
            model_path="./.models/Meta-Llama-3-8B-Instruct.Q5_K_M.gguf",
            n_ctx=4096,
            n_batch=64,
            temperature=TEMPERATURE,
            verbose=False
        )

    elif modelo_llm == "Ollama (servidor)":
        base_url = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        return OllamaLLM(
            model=LLM_MODEL,
            base_url=base_url,
            temperature=TEMPERATURE
        )

    elif modelo_llm == "OpenAI (API)":
        if not openai_key:
            raise ValueError("OPENAI_API_KEY não definido no ambiente.")
        return ChatOpenAI(
            model=OPENAI_MODEL,
            temperature=TEMPERATURE,
            api_key=openai_key
        )

    else:
        raise ValueError(f"Modelo LLM desconhecido: {modelo_llm}")
