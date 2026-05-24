import re

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from app.agents.groq_llm import llm


def clean_response(text: str):
    text = re.sub(r"\*\*", "", text)
    text = re.sub(r"\*", "", text)
    return text.strip()


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_store = FAISS.load_local(
    "app/rag/faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)


def document_assistant_agent(question: str):

    docs = vector_store.similarity_search(
        question,
        k=3
    )

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
You are a Document Assistant Agent for a Smart Retail Assistant.

Use only the provided retail knowledge base context to answer the question.

Context:
{context}

User Question:
{question}

Rules:
- Answer clearly and professionally.
- Do not use markdown symbols.
- Do not use asterisks.
- If answer is not available in context, say the knowledge base does not contain that information.
"""

    response = llm.invoke(prompt)

    return clean_response(response.content)