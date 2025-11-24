import pandas as pd
from backend.database.db_models import Order
from backend.database.db_setup import SessionLocal
import os

#Loading the data file and data transformations
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "data", "orders.csv")
df_orders = pd.read_csv(CSV_PATH)
df_orders["date"] = pd.to_datetime(df_orders["date"])


mappings = [
    {
    "order_id": row.order_id,
    "order_date": row.date,
    "customer_id": row.customer_id,
    "amount": row.amount

    }
    for row in df_orders.itertuples(index=False)]

with SessionLocal() as session:
    session.bulk_insert_mappings(Order, mappings)
    session.commit()

session.close()
print("Orders loaded to the db")

