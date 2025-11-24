from celery import Celery
import requests
from datetime import datetime
from celery.schedules import crontab

# Celery app for scheduling the ETL integration (Task 3)
app = Celery('etl_app', broker='redis://localhost:6379/0')



@app.task
def etl_job():

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file_path = f"task3_log_{timestamp}.txt"

    print("Running ETL")

    # Fetching the JSON payload for all active customers (must have the FastAPI app running on port 8003
    response = requests.get("http://127.0.0.1:8003/customers?status=active")
    if response.status_code != 200:
        raise Exception(f"Failed to fetch customers: {response.status_code}")
    customers = response.json()
    print(f"Fetched {len(customers)} active customers")

    target_api = "https://postman-echo.com/post"

    # Logging each outgoing request's status code
    with open(log_file_path, "a") as log_file:
        for customer in customers:
            customer['name'] = customer['firstname'] + " " + customer['surname']

            cust_json = {
                "customer_id": customer['customer_id'],
                "name": customer['name'],
                "email": customer['email'],
                "address": customer['address'],
                "zipcode": customer['zipcode'],
                "region": customer['region'],
                "status": customer['status']

            }
            # Sending the transformed record to the target API
            response = requests.post(target_api, json=cust_json, timeout=5)
            print(f"Customer {customer['customer_id']} sent, response code: {response.status_code}")

            log_file.write(f"Customer {customer['customer_id']} sent, response code: {response.status_code}\n")



# Celery Beat schedule
app.conf.beat_schedule = {
    'run-every-30-seconds': {
        'task': 'backend.api.schedule_etl.etl_job',
        'schedule': 30.0,  # Every 30 seconds
        # cron timer : 'schedule' : crontab(minute=0) ETL schedule for every hour every day (Prod replacement)
    }
}
app.conf.timezone = 'UTC'
