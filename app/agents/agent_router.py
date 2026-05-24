from app.agents.data_analyst_agent import data_analyst_agent
from app.agents.document_agent import document_assistant_agent
from app.agents.ml_expert_agent import ml_expert_agent


def route_question(question: str):

    question_lower = question.lower()

    document_keywords = [
        "policy",
        "return",
        "refund",
        "inventory rule",
        "low stock",
        "customer support",
        "promotion policy",
        "reorder"
    ]

    ml_keywords = [
        "model",
        "forecast",
        "prediction",
        "xgboost",
        "lag",
        "rmse",
        "mae",
        "wmape",
        "r2",
        "anomaly",
        "isolation forest",
        "feature importance"
    ]

    data_keywords = [
        "sales",
        "store",
        "department",
        "top performing",
        "highest",
        "average",
        "total",
        "analytics"
    ]

    if any(keyword in question_lower for keyword in document_keywords):
        selected_agent = "Document Assistant Agent"
        answer = document_assistant_agent(question)

    elif any(keyword in question_lower for keyword in ml_keywords):
        selected_agent = "ML Expert Agent"
        answer = ml_expert_agent(question)

    elif any(keyword in question_lower for keyword in data_keywords):
        selected_agent = "Data Analyst Agent"
        answer = data_analyst_agent(question)

    else:
        selected_agent = "Data Analyst Agent"
        answer = data_analyst_agent(question)

    return {
        "selected_agent": selected_agent,
        "answer": answer
    }