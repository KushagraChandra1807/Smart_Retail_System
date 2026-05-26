from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from azure.ai.ml.entities import Model
from azure.ai.ml.constants import AssetTypes

SUBSCRIPTION_ID = "1ff2bf19-24b1-4e18-84c0-afb8fb576d63"
RESOURCE_GROUP = "Sprint_Capstone"
WORKSPACE_NAME = "smart-retail-ml"

MODEL_PATH = "app/ml/demand_forecast_model.pkl"

ml_client = MLClient(
    DefaultAzureCredential(),
    SUBSCRIPTION_ID,
    RESOURCE_GROUP,
    WORKSPACE_NAME
)

model = Model(
    path=MODEL_PATH,
    name="smart-retail-demand-forecast-model",
    description="XGBoost demand forecasting model for Smart Retail Assistant",
    type=AssetTypes.CUSTOM_MODEL
)

registered_model = ml_client.models.create_or_update(model)

print("Model registered successfully!")
print("Model name:", registered_model.name)
print("Model version:", registered_model.version)