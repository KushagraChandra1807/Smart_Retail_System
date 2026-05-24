import pandas as pd
import re

from app.agents.groq_llm import llm

train_df = pd.read_csv("app/ml/train.csv")


def clean_response(text: str):
    text = re.sub(r"\*\*", "", text)
    text = re.sub(r"\*", "", text)
    return text.strip()


def generate_sales_summary():

    total_sales = round(
        train_df["Weekly_Sales"].sum(),
        2
    )

    avg_sales = round(
        train_df["Weekly_Sales"].mean(),
        2
    )

    top_store = (
        train_df.groupby("Store")["Weekly_Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(1)
    )

    top_department = (
        train_df.groupby("Dept")["Weekly_Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(1)
    )

    return {
        "total_sales": total_sales,
        "average_sales": avg_sales,
        "top_store": int(top_store.index[0]),
        "top_store_sales": round(float(top_store.iloc[0]), 2),
        "top_department": int(top_department.index[0]),
        "top_department_sales": round(float(top_department.iloc[0]), 2)
    }


def data_analyst_agent(question: str):

    summary = generate_sales_summary()

    prompt = f"""
You are a Retail Data Analyst AI Agent.

Use the retail analytics summary below to answer the user question.

Retail Analytics Summary:
Total Sales: {summary["total_sales"]}
Average Weekly Sales: {summary["average_sales"]}
Top Performing Store: Store {summary["top_store"]}
Top Store Sales: {summary["top_store_sales"]}
Top Performing Department: Department {summary["top_department"]}
Top Department Sales: {summary["top_department_sales"]}

User Question:
{question}

Rules:
- Give a clear business answer.
- Do not use markdown symbols.
- Do not use asterisks.
- Keep answer simple and professional.
"""

    response = llm.invoke(prompt)

    return clean_response(response.content)