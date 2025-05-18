from langchain.prompts import PromptTemplate

def get_custom_prompt():
    return PromptTemplate(
        input_variables=["context", "question"],
        template="""
Você é um assistente que responde **somente com base nas evidências abaixo**, sem adicionar opiniões ou interpretações.

🔹 **Trechos disponíveis:**
{context}

🔹 **Pergunta:**
{question}

💡 **Instruções obrigatórias**:
- Se a resposta estiver escrita **explicitamente nos trechos**, repita-a **exatamente** como está. 
- **Não altere o significado** do texto fornecido.
- Se a resposta **não estiver presente literalmente**, diga: **"Os documentos não fornecem essa informação."**
- **Não deduza, não interprete, não invente.**
- Sempre cite o trecho exato do documento ao responder.

📝 **Resposta**:
"""
    )

