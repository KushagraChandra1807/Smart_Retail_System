from fastapi import APIRouter
from app.azure_foundry.foundry_agent_architecture import get_foundry_architecture

router = APIRouter()


@router.get("/azure-foundry-architecture")
def azure_foundry_architecture():
    return {
        "message": "Azure AI Foundry-style agent architecture for Smart Retail Assistant",
        "architecture": get_foundry_architecture(),
        "status": "success"
    }