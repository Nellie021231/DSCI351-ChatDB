import pandas as pd
from sqlalchemy import create_engine
import os
import kagglehub

engine = create_engine('mysql+pymysql://root@localhost:3306/project')

# check if datasets exist, otherwise download
def get_dataset_path(dataset_id):
    base_cache = os.path.expanduser("~/.cache/kagglehub/datasets")
    dataset_path = os.path.join(base_cache, dataset_id.replace("/", os.sep), "latest")
    if os.path.exists(dataset_path):
        print(f" Using cached dataset: {dataset_id}")
        return dataset_path
    else:
        print(f" Downloading dataset: {dataset_id}")
        return kagglehub.dataset_download(dataset_id)

# three datasets paths
customer_path = get_dataset_path("mateusxavier/customer-analysis")
startup_path = get_dataset_path("justinas/startup-investments")
grocery_path = get_dataset_path("andrexibiza/grocery-sales-dataset")

datasets = {
    "customer_analysis": {
        "path": customer_path,
        "tables": ["customers", "marketing_interactions", "subscriptions", "transactions"]
    },
    "startup_investments": {
        "path": startup_path,
        "tables": ["acquisitions", "degrees", "funding_rounds", "funds", "investments",
                   "ipos", "milestones", "objects", "offices", "people", "relationships"]
    },
    "grocery_sales": {
        "path": grocery_path,
        "tables": ["categories", "cities", "countries", "customers", "employees", "products", "sales"]
    }
}

print("\n Starting data import\n")

for db_prefix, info in datasets.items():
    path = info["path"]
    for table in info["tables"]:
        file_path = os.path.join(path, f"{table}.csv")
        table_name = f"{db_prefix}_{table}"
        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                df.to_sql(table_name, con=engine, if_exists="replace", index=False)
                print(f" Imported `{table_name}` from {file_path}")
            except Exception as e:
                print(f" Failed to import {table_name}: {e}")
        else:
            print(f"️ File not found: {file_path}")

print("\n All datasets imported successfully.")
