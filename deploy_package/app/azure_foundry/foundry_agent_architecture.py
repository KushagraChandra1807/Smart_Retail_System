"""
Azure AI Foundry-Style Agent Architecture
Smart Retail Assistant

This file documents how the Smart Retail Assistant maps to an Azure AI Foundry
multi-agent deployment pattern.

Azure AI Foundry Integration:
- Data Analyst Agent: answers retail sales analytics questions
- Document Assistant Agent: answers policy/document/RAG questions
- ML Expert Agent: explains forecasting and anomaly detection outputs
- Agent Router: selects the best agent based on user query

This supports the Azure AI & Cloud syllabus requirement:
"Azure AI Foundry for deployment patterns"
"""

SMART_RETAIL_FOUNDRY_ARCHITECTURE = {
    "project_name": "Smart Retail Assistant",
    "azure_service": "Azure AI Foundry",
    "deployment_pattern": "Multi-Agent GenAI Orchestration",
    "agents": [
        {
            "agent_name": "Data Analyst Agent",
            "role": "Analyzes retail sales, store performance, and business KPIs",
            "fastapi_route": "/ask-data-agent",
            "input": "User asks sales or business analytics question",
            "output": "Retail insight based on analytics data"
        },
        {
            "agent_name": "Document Assistant Agent",
            "role": "Uses RAG to answer questions from retail policy documents",
            "fastapi_route": "/ask-document-agent",
            "input": "User asks document or policy-related question",
            "output": "Answer retrieved from vector store knowledge base"
        },
        {
            "agent_name": "ML Expert Agent",
            "role": "Explains forecasting, anomaly detection, and ML model outputs",
            "fastapi_route": "/ask-ml-agent",
            "input": "User asks ML or forecasting-related question",
            "output": "Explanation of ML prediction or feature importance"
        },
        {
            "agent_name": "Agent Router",
            "role": "Selects the correct agent based on user intent",
            "fastapi_route": "/ask-agent",
            "input": "Any user question",
            "output": "Routes request to best agent and returns final response"
        }
    ],
    "cloud_mapping": {
        "Azure AI Foundry": "Used as the enterprise deployment and orchestration pattern for GenAI agents",
        "Azure Document Intelligence": "Used for invoice and document extraction",
        "Azure ML Workspace": "Used for registering the forecasting ML model",
        "Environment Variables": "Used for secure API keys and endpoints"
    }
}


def get_foundry_architecture():
    return SMART_RETAIL_FOUNDRY_ARCHITECTURE