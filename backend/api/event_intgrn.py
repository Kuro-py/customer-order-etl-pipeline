from celery import Celery
import json
import os
from datetime import datetime

app = Celery('etl_app', broker='redis://localhost:6379/0')


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "order_events")
@app.task
def order_created_event(order_data):

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"order_{order_data['order_id']}_{timestamp}.txt"
    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, "w") as f:
        f.write(json.dumps(order_data, indent=4))

    return f"Order created and saved in: {filename}"

