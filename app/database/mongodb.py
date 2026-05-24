from pymongo import MongoClient
from dotenv import load_dotenv
import os

# -----------------------------------
# LOAD ENV VARIABLES
# -----------------------------------

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# -----------------------------------
# DEBUGGING
# -----------------------------------

print("MONGO URI =", MONGO_URI)
print("DATABASE NAME =", DATABASE_NAME)

# -----------------------------------
# CONNECT TO MONGODB
# -----------------------------------

client = MongoClient(MONGO_URI)

db = client[DATABASE_NAME]

# -----------------------------------
# COLLECTIONS
# -----------------------------------

sales_collection = db["sales"]

forecast_collection = db["forecasts"]

print("MongoDB Atlas Connected Successfully!")