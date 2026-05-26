import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

AZURE_LIGHT_MODE = os.getenv("AZURE_LIGHT_MODE", "false").lower() == "true"

app = FastAPI(
    title="Smart Retail Assistant API",
    description="AI-powered Smart Retail Assistant with Azure integration",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# LIGHTWEIGHT ROUTES - safe for Azure startup
from app.routes.document_intelligence_routes import router as document_intelligence_router
from app.routes.azure_foundry_routes import router as azure_foundry_router

app.include_router(document_intelligence_router)
app.include_router(azure_foundry_router)

# HEAVY ROUTES - only load locally, not on Azure
if not AZURE_LIGHT_MODE:
    from app.routes.data_engineering_routes import router as data_engineering_router
    from app.routes.agent_routes import router as agent_router

    app.include_router(data_engineering_router)
    app.include_router(agent_router)


@app.get("/")
def health():
    return {
        "status": "running",
        "project": "Smart Retail Assistant",
        "deployment": "Azure Web App",
        "azure_light_mode": AZURE_LIGHT_MODE
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "Smart Retail Assistant API is working"
    }