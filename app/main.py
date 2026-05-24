from fastapi import FastAPI

from app.routes.sales_routes import router as sales_router
from app.routes.anomaly_routes import router as anomaly_router
from app.routes.agent_routes import router as agent_router

app = FastAPI(
    title="Smart Retail Assistant",
    description="Enterprise Retail Forecasting and Anomaly Detection System",
    version="1.0.0"
)

# -----------------------------------
# REGISTER ROUTES
# -----------------------------------

app.include_router(
    sales_router,
    tags=["Sales Forecasting APIs"]
)

app.include_router(
    anomaly_router,
    tags=["Anomaly Detection APIs"]
)

app.include_router(
    agent_router,
    tags=["AI Agent APIs"]
)

# -----------------------------------
# HOME ROUTE
# -----------------------------------

@app.get("/")
def home():

    return {
        "message": "Smart Retail Assistant API Running Successfully",
        "features": [
            "Demand Forecasting",
            "Retail Anomaly Detection",
            "Sales Analytics",
            "Enterprise Retail Intelligence"
        ],
        "status": "ACTIVE"
    }

# -----------------------------------
# HEALTH CHECK
# -----------------------------------

@app.get("/health")
def health_check():

    return {
        "server": "running",
        "api_status": "healthy"
    }