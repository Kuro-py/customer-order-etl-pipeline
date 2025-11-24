import pandas as pd
from backend.database.db_models import Customer
from backend.database.db_setup import SessionLocal
import os

#Loading the data file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "data", "customers.csv")
df_customers = pd.read_csv(CSV_PATH)


mappings = [
    {
        "customer_id": row.customer_id,
    "firstname": row.firstname,
    "surname": row.surname,
    "email": row.email,
    "address": row.address,
    "zipcode": row.zip_code,
    "region": row.region,
    "status": row.status
    }
    for row in df_customers.itertuples(index=False)]

with SessionLocal() as session:
    session.bulk_insert_mappings(Customer, mappings)
    session.commit()

session.close()
print("Customers loaded to the db")
