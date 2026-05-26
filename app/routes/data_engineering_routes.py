from fastapi import APIRouter

router = APIRouter()


@router.get("/data-pipeline-summary")
def data_pipeline_summary():

    return {
        "message": "Azure Data Engineering Pipeline Summary",
        "pipeline_status": "success",
        "project": "Smart Retail Assistant",

        "raw_layer": {
            "tool": "Azure Data Factory",
            "storage": "Azure Storage raw container",
            "datasets": [
                "train.csv",
                "features.csv",
                "stores.csv"
            ]
        },

        "staged_layer": {
            "tool": "Azure Data Factory Copy Data Activity",
            "storage": "Azure Storage staged container",
            "datasets": [
                "train_staged.csv",
                "features_staged.csv",
                "stores_staged.csv"
            ]
        },

        "curated_layer": {
            "tool": "Azure Databricks with PySpark",
            "tables": [
                "retail_curated_delta",
                "retail_curated_parquet",
                "store_sales_summary"
            ],
            "storage_format": [
                "Delta Table",
                "Parquet Table"
            ]
        },

        "transformations": [
            "Merged train, features, and stores datasets",
            "Removed duplicate records",
            "Handled missing values",
            "Created Sales_Category feature",
            "Created Demand_Flag feature",
            "Generated Spark SQL sales summary"
        ],

        "technologies": [
            "Azure Data Factory",
            "Azure Databricks",
            "PySpark",
            "Spark SQL",
            "Delta Lake",
            "Parquet Storage"
        ],

        "syllabus_mapping": {
            "ADF": "Raw data ingestion",
            "Databricks": "PySpark transformation",
            "Spark_SQL": "Analytics query engine",
            "Delta_Parquet": "Curated storage layer",
            "Raw_Staged_Curated": "Implemented successfully"
        }
    }