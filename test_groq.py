from app.agents.groq_llm import llm

response = llm.invoke(
    "Say hello and confirm you are ready for Smart Retail Assistant project."
)

print(response.content)