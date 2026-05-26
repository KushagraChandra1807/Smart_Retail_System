from fastapi import FastAPI

app = FastAPI(
    title="Smart Retail Assistant API",
    description="Azure lightweight deployment",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "status": "running",
        "project": "Smart Retail Assistant",
        "deployment": "Azure Web App"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

@app.get("/azure-foundry-architecture")
def azure_foundry_architecture():
    return {
        "message": "Azure AI Foundry-style agent architecture for Smart Retail Assistant",
        "status": "success"
    }

@app.get("/data-pipeline-summary")
def data_pipeline_summary():
    return {
        "message": "Azure Data Engineering Pipeline Summary",
        "pipeline_status": "success",
        "raw_layer": ["train.csv", "features.csv", "stores.csv"],
        "staged_layer": ["train_staged.csv", "features_staged.csv", "stores_staged.csv"],
        "curated_layer": ["retail_curated_delta", "retail_curated_parquet", "store_sales_summary"],
        "technologies": ["Azure Data Factory", "Azure Databricks", "PySpark", "Spark SQL", "Delta Lake", "Parquet"]
    }