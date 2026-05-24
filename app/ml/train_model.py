import pandas as pd
import numpy as np
import joblib

from xgboost import XGBRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# -----------------------------------
# LOAD DATASETS
# -----------------------------------

train_df = pd.read_csv("app/ml/train.csv")

features_df = pd.read_csv("app/ml/features.csv")

stores_df = pd.read_csv("app/ml/stores.csv")

print("\nDatasets Loaded Successfully!")

# -----------------------------------
# MERGE DATASETS
# -----------------------------------

df = train_df.merge(
    features_df,
    on=["Store", "Date", "IsHoliday"],
    how="left"
)

df = df.merge(
    stores_df,
    on="Store",
    how="left"
)

print("\nMerged Dataset Shape:", df.shape)

# -----------------------------------
# DATA CLEANING
# -----------------------------------

# Fill markdown null values
markdown_cols = [
    "MarkDown1",
    "MarkDown2",
    "MarkDown3",
    "MarkDown4",
    "MarkDown5"
]

for col in markdown_cols:
    df[col] = df[col].fillna(0)

# Fill economic null values
df["CPI"] = df["CPI"].fillna(
    df["CPI"].median()
)

df["Unemployment"] = df["Unemployment"].fillna(
    df["Unemployment"].median()
)

# -----------------------------------
# DATE FEATURE ENGINEERING
# -----------------------------------

df["Date"] = pd.to_datetime(df["Date"])

df["Year"] = df["Date"].dt.year

df["Month"] = df["Date"].dt.month

df["Week"] = df["Date"].dt.isocalendar().week.astype(int)

df["Day"] = df["Date"].dt.day

df["DayOfWeek"] = df["Date"].dt.dayofweek

df["Quarter"] = df["Date"].dt.quarter

df["IsMonthStart"] = df["Date"].dt.is_month_start.astype(int)

df["IsMonthEnd"] = df["Date"].dt.is_month_end.astype(int)

# -----------------------------------
# ENTERPRISE WEATHER FEATURES
# -----------------------------------

# Simulated humidity
df["Humidity"] = (
    70 - (df["Temperature"] * 0.3)
).clip(20, 100)

# Simulated rainfall
df["Rainfall"] = np.where(
    df["Temperature"] < 50,
    np.random.uniform(2, 10, len(df)),
    np.random.uniform(0, 5, len(df))
)

# Simulated wind speed
df["WindSpeed"] = np.random.uniform(
    5,
    25,
    len(df)
)

# Temperature change trend
df["Temp_Change"] = df.groupby(
    "Store"
)["Temperature"].diff().fillna(0)

# Extreme weather flag
df["ExtremeWeather"] = np.where(
    (df["Temperature"] < 32) |
    (df["Temperature"] > 95),
    1,
    0
)

# -----------------------------------
# SORT FOR TIME SERIES
# -----------------------------------

df = df.sort_values(
    by=["Store", "Dept", "Date"]
)

# -----------------------------------
# LAG FEATURES
# -----------------------------------

df["Lag_1"] = df.groupby(
    ["Store", "Dept"]
)["Weekly_Sales"].shift(1)

df["Lag_2"] = df.groupby(
    ["Store", "Dept"]
)["Weekly_Sales"].shift(2)

df["Lag_4"] = df.groupby(
    ["Store", "Dept"]
)["Weekly_Sales"].shift(4)

# -----------------------------------
# ROLLING MEAN FEATURES
# -----------------------------------

df["Rolling_Mean_4"] = df.groupby(
    ["Store", "Dept"]
)["Weekly_Sales"].transform(
    lambda x: x.shift(1).rolling(4).mean()
)

df["Rolling_Mean_8"] = df.groupby(
    ["Store", "Dept"]
)["Weekly_Sales"].transform(
    lambda x: x.shift(1).rolling(8).mean()
)

# -----------------------------------
# EXPONENTIAL MOVING AVERAGE
# -----------------------------------

df["EMA_4"] = df.groupby(
    ["Store", "Dept"]
)["Weekly_Sales"].transform(
    lambda x: x.shift(1).ewm(span=4).mean()
)

# -----------------------------------
# SALES TREND FEATURE
# -----------------------------------

df["Sales_Trend"] = (
    df["Lag_1"] - df["Lag_2"]
)

# -----------------------------------
# REMOVE NULLS FROM LAG FEATURES
# -----------------------------------

df.dropna(inplace=True)

print("\nDataset After Feature Engineering:", df.shape)

# -----------------------------------
# ENCODE STORE TYPE
# -----------------------------------

df["Type"] = df["Type"].map({
    "A": 1,
    "B": 2,
    "C": 3
})

# -----------------------------------
# FEATURES & TARGET
# -----------------------------------

features = [
    # Store Features
    "Store",
    "Dept",
    "Type",
    "Size",

    # Holiday & Economic
    "IsHoliday",
    "Fuel_Price",
    "CPI",
    "Unemployment",

    # Temperature & Weather
    "Temperature",
    "Humidity",
    "Rainfall",
    "WindSpeed",
    "Temp_Change",
    "ExtremeWeather",

    # Promotions
    "MarkDown1",
    "MarkDown2",
    "MarkDown3",
    "MarkDown4",
    "MarkDown5",

    # Date Features
    "Year",
    "Month",
    "Week",
    "Day",
    "DayOfWeek",
    "Quarter",
    "IsMonthStart",
    "IsMonthEnd",

    # Time-Series Features
    "Lag_1",
    "Lag_2",
    "Lag_4",
    "Rolling_Mean_4",
    "Rolling_Mean_8",
    "EMA_4",
    "Sales_Trend"
]

X = df[features]

y = df["Weekly_Sales"]

# -----------------------------------
# TIME SERIES SPLIT
# -----------------------------------

split_index = int(len(df) * 0.8)

X_train = X.iloc[:split_index]

X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]

y_test = y.iloc[split_index:]

print("\nTraining Samples:", len(X_train))

print("Testing Samples:", len(X_test))

# -----------------------------------
# XGBOOST MODEL
# -----------------------------------

print("\nTraining Enterprise XGBoost Model...")

model = XGBRegressor(
    n_estimators=500,
    learning_rate=0.03,
    max_depth=10,
    min_child_weight=3,
    subsample=0.8,
    colsample_bytree=0.8,
    gamma=0.1,
    reg_alpha=0.1,
    reg_lambda=1,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

print("Model Training Completed!")

# -----------------------------------
# MODEL EVALUATION
# -----------------------------------

predictions = model.predict(X_test)

mae = mean_absolute_error(
    y_test,
    predictions
)

mse = mean_squared_error(
    y_test,
    predictions
)

rmse = np.sqrt(mse)

r2 = r2_score(
    y_test,
    predictions
)

# MAPE
# SAFE MAPE

non_zero_mask = y_test != 0

mape = np.mean(
    np.abs(
        (
            y_test[non_zero_mask] -
            predictions[non_zero_mask]
        ) / y_test[non_zero_mask]
    )
) * 100

print("\nModel Evaluation")
print("---------------------------")

print("MAE   :", round(mae, 2))

print("MSE   :", round(mse, 2))

print("RMSE  :", round(rmse, 2))

# Weighted MAPE

wmape = (
    np.sum(np.abs(y_test - predictions))
    / np.sum(np.abs(y_test))
) * 100

print("WMAPE :", round(wmape, 2), "%")

print("R2 Score :", round(r2, 4))

# -----------------------------------
# FEATURE IMPORTANCE
# -----------------------------------

importance_df = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
})

importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
)

print("\nTop 15 Important Features")
print("---------------------------")

print(importance_df.head(15))

# -----------------------------------
# SAVE MODEL
# -----------------------------------

joblib.dump(
    model,
    "app/ml/demand_forecast_model.pkl"
)

print("\nEnterprise XGBoost Model Saved Successfully!")