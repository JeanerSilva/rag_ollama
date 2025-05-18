from langchain.prompts import PromptTemplate

def get_custom_prompt():
    return PromptTemplate(
        input_variables=["context", "question"],
        template="""
Você é um assistente com acesso a trechos de documentos oficiais.

Seu trabalho é responder com base **exclusivamente no conteúdo abaixo**, sem adicionar informações externas.

🔹 **Trechos disponíveis:**
{context}

🔹 **Pergunta:**
{question}

💡 **Instruções para resposta**:
- Se a resposta estiver expressa literalmente nos trechos, repita-a com clareza.
- Seja direto e conciso.
- Se os trechos não contêm a resposta, apenas diga: "Os documentos não fornecem essa informação.
- Se houver múltiplos objetivos, liste **todos** que forem mencionados nos documentos. Não se limite aos primeiros encontrados.
"

📝 **Resposta**:
"""
    )
