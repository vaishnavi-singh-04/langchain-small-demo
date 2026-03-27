from langchain_core.prompts import ChatPromptTemplate

def get_prompt():
    return ChatPromptTemplate.from_template("""
You are a helpful assistant.

Answer ONLY using the context below.

Context:
{context}

Question:
{question}
""")