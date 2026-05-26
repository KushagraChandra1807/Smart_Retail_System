import re

from app.agents.groq_llm import llm


def clean_response(text: str):
    text = re.sub(r"\*\*", "", text)
    text = re.sub(r"\*", "", text)
    return text.strip()


def ml_expert_agent(question: str):

    model_context = """
Smart Retail Assistant ML System:

Forecasting Model:
- Model Used: XGBoost Regressor
- Dataset: Walmart Store Sales Forecasting Dataset
- Task: Weekly sales demand forecasting
- R2 Score: 0.9671
- WMAPE: 7.94%
- MAE: 1024.15
- RMSE: 3471.33

Important Forecasting Features:
- Lag_1: previous week sales
- EMA_4: recent sales trend
- Rolling_Mean_4: 4-week moving average
- Lag_4: monthly sales memory
- IsHoliday: holiday demand effect
- MarkDown3: promotion impact
- Week and Month: seasonality
- Dept and Store Type: retail structure

Anomaly Detection Model:
- Model Used: Isolation Forest
- Task: Detect unusual weekly sales patterns
- Total anomalies detected: 8432
- Use cases: sales spikes, abnormal demand, possible fraud, unusual promotion impact, inventory alerts

Business Meaning:
- High forecast means higher expected weekly demand.
- Anomaly means sales behavior is unusual compared to normal store and department patterns.
- Lag and rolling features are important because retail demand depends strongly on recent sales history.
"""

    prompt = f"""
You are an ML Expert Agent for a Smart Retail Assistant.

Use the ML system context below to answer the user's question.

ML System Context:
{model_context}

User Question:
{question}

Rules:
- Explain in simple business language.
- Do not use markdown symbols.
- Do not use asterisks.
- Keep the answer professional and clear.
"""

    response = llm.invoke(prompt)

    return clean_response(response.content)