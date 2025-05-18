from langchain.prompts import PromptTemplate

def get_custom_prompt():
    return PromptTemplate(
        input_variables=["context", "question"],
        template="""
Você é um assistente especializado em responder perguntas com base apenas nos trechos fornecidos abaixo. 

🔹 **Trechos disponíveis:**
{context}

🔹 **Pergunta:**
{question}

💡 **Instruções obrigatórias**:
- Responda com base apenas no conteúdo dos trechos.
- Se a resposta estiver claramente presente, repita-a.
- Se a informação **não aparecer em nenhum trecho**, diga: **"Os documentos não fornecem essa informação."**
- **Não invente, nem adicione interpretações próprias.**
- Para respostas curtas ou frases exatas, apenas repita a frase do trecho.

📝 **Resposta**:
"""
    )

