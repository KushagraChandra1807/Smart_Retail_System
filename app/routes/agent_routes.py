from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.agents.data_analyst_agent import data_analyst_agent
from app.agents.document_agent import document_assistant_agent

from app.agents.ml_expert_agent import ml_expert_agent

from app.agents.agent_router import route_question

router = APIRouter()


class AgentQuestion(BaseModel):
    question: str


@router.post("/ask-data-agent")
def ask_data_agent(request: AgentQuestion):

    try:
        answer = data_analyst_agent(request.question)

        return {
            "agent": "Data Analyst Agent",
            "question": request.question,
            "answer": answer,
            "status": "success"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Agent failed: {str(e)}"
        )
    
@router.post("/ask-document-agent")
def ask_document_agent(request: AgentQuestion):

    try:
        answer = document_assistant_agent(request.question)

        return {
            "agent": "Document Assistant Agent",
            "question": request.question,
            "answer": answer,
            "status": "success"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Document agent failed: {str(e)}"
        )
@router.post("/ask-ml-agent")
def ask_ml_agent(request: AgentQuestion):

    try:
        answer = ml_expert_agent(request.question)

        return {
            "agent": "ML Expert Agent",
            "question": request.question,
            "answer": answer,
            "status": "success"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"ML agent failed: {str(e)}"
        )
    
@router.post("/ask-agent")
def ask_agent(request: AgentQuestion):

    try:
        result = route_question(request.question)

        return {
            "question": request.question,
            "selected_agent": result["selected_agent"],
            "answer": result["answer"],
            "status": "success"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Agent router failed: {str(e)}"
        )