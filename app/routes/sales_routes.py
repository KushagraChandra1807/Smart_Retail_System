from fastapi import APIRouter, HTTPException

from app.models.sales_model import SalesData
from app.database.mongodb import sales_collection
from app.services.forecast_service import predict_sales
from app.utils.logger import logger

router = APIRouter()

# -----------------------------------
# API 1 - DATA INGESTION
# -----------------------------------

@router.post("/upload-sales")
def upload_sales(data: SalesData):

    try:

        sales_collection.insert_one(
            data.model_dump()
        )

        logger.info(
            "Sales data inserted successfully"
        )

        return {
            "message": "Sales data uploaded successfully",
            "data": data.model_dump()
        }

    except Exception as e:

        logger.error(
            f"Upload Error: {str(e)}"
        )

        raise HTTPException(
            status_code=500,
            detail=f"Error uploading sales data: {str(e)}"
        )

# -----------------------------------
# API 2 - ENTERPRISE DEMAND FORECAST
# -----------------------------------

@router.get("/forecast")
def forecast(

    store: int,
    dept: int,

    temperature: float,

    fuel_price: float,

    cpi: float,

    unemployment: float,

    size: int,

    is_holiday: int,

    month: int,

    week: int,

    day: int,

    lag_1: float,

    lag_2: float,

    rolling_mean_4: float,

    ema_4: float
):

    try:

        prediction = predict_sales(

            store,
            dept,
            temperature,
            fuel_price,
            cpi,
            unemployment,
            size,
            is_holiday,
            month,
            week,
            day,
            lag_1,
            lag_2,
            rolling_mean_4,
            ema_4
        )

        logger.info(
            f"Forecast generated for Store {store}"
        )

        return {

            "forecasted_sales": prediction,

            "model": "Enterprise XGBoost",

            "status": "success",

            "inputs": {

                "store": store,
                "dept": dept,
                "temperature": temperature,
                "fuel_price": fuel_price,
                "cpi": cpi,
                "unemployment": unemployment,
                "size": size,
                "is_holiday": is_holiday,
                "month": month,
                "week": week,
                "day": day,
                "lag_1": lag_1,
                "lag_2": lag_2,
                "rolling_mean_4": rolling_mean_4,
                "ema_4": ema_4
            }
        }

    except Exception as e:

        logger.error(
            f"Forecast Error: {str(e)}"
        )

        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )