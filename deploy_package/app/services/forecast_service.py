import joblib
import pandas as pd

# -----------------------------------
# LOAD TRAINED MODEL
# -----------------------------------

model = joblib.load(
    "app/ml/demand_forecast_model.pkl"
)

# -----------------------------------
# PREDICTION FUNCTION
# -----------------------------------

def predict_sales(
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
):

    # -----------------------------------
    # CREATE INPUT DATAFRAME
    # -----------------------------------

    input_data = pd.DataFrame([{

        "Store": store,
        "Dept": dept,

        "Type": 1,

        "Size": size,

        "IsHoliday": is_holiday,

        "Fuel_Price": fuel_price,

        "CPI": cpi,

        "Unemployment": unemployment,

        "Temperature": temperature,

        "Humidity": 65,

        "Rainfall": 0,

        "WindSpeed": 12,

        "Temp_Change": 2,

        "ExtremeWeather": 0,

        "MarkDown1": 0,
        "MarkDown2": 0,
        "MarkDown3": 0,
        "MarkDown4": 0,
        "MarkDown5": 0,

        "Year": 2026,

        "Month": month,

        "Week": week,

        "Day": day,

        "DayOfWeek": 2,

        "Quarter": 2,

        "IsMonthStart": 0,

        "IsMonthEnd": 0,

        "Lag_1": lag_1,

        "Lag_2": lag_2,

        "Lag_4": lag_2,

        "Rolling_Mean_4": rolling_mean_4,

        "Rolling_Mean_8": rolling_mean_4,

        "EMA_4": ema_4,

        "Sales_Trend": 1.05
    }])

    # -----------------------------------
    # PREDICT
    # -----------------------------------

    prediction = model.predict(input_data)

    return round(float(prediction[0]), 2)