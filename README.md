Project: Customer & Orders ETL & Event-Driven Pipeline

--Prerequisites
--------------------------------------
Python 3.9+ installed

Redis running locally on the default port (for Celery):
  Host: 127.0.0.1
  Port: 6379
  
Python packages to be installed:
	pip install fastapi uvicorn sqlalchemy pandas requests celery redis


Tasks :
Task 1 
Use the Customer and Order CSV files to create corresponding tables in a
database.
Task 2
Build a simple API on top of this data. This API should provide 3 REST endpoints.
The REST endpoints should be as follows:
● One that returns Customer and Order data for all Customers. This endpoint
should also allow you to query for all active or archived Customers.
● Another that returns the same data for a single Customer using a Customer
id.
● Another that is a create Order endpoint.
Task 3
Build an Integration that could be run on a schedule, for example as an ETL job.
This should call the first endpoint of your API above to:
● Return the JSON payload for all active customers.
● Then transform the data by concatenating “firstname” and “surname” fields
into a single “name” field.
● Then send all the data onwards to a target API that only accepts a payload
with a single customer record.
● Then log the returned HTTP Response Code.
You can use https://postman-echo.com/post as the target API endpoint.
Task 4
Build a basic Event Driven Integration.
● Add capability to your stack to capture created orders and send each create
event as a single message to a Simple Queue based system.
● Then add functionality to process these queued messages and save each one
as an individual text file.
● Then create some new orders and see the files being created.

--Create DB and Load CSVs
----------------------------------------

Create a local SQLite database (etl_local.db) and populate it with customers and orders from CSV.

(All the files related to db are in .\etl-pipeline\backend\database. etl_local.db are gets created in the same folder
Data files are in .\etl-pipeline\backend\database\data)



1. Ensure you are in the project root (the folder that contains `backend\`).

2. Initialize the database schema (tables):

    python -m backend.database._init_db / Run the script directly from your interpretor 


   This uses:
   - `db_setup.py` for the engine and Base.
   - `db_models.py` for the Customer and Order models.
   - `_init_db.py` to call `Base.metadata.create_all()`

3. Load customers from CSV into the `customers` table: 

    python -m backend.database.load_customers / Run the script directly from your interpretor 

4. Load orders from CSV into the `orders` table:

    python -m backend.database.load_orders / Run the script directly from your interpretor 
	
[If required I have left a pre-built db as "cache_etl_local", it can be used after removing the prefix]

Run the REST API
-----------------------

(Code files related to api, task 3 and task 4 are in \etl-pipeline\backend\api)

To run the API:

1. From the project root, start Uvicorn:

    uvicorn backend.api.main:app --reload --port 8003

2. Endpoints:
   - `GET http://127.0.0.1:8003/customers`
   - `GET http://127.0.0.1:8003/customers/{customer_id}`
   - Navigate to FastAPI docs : http://127.0.0.1:8003/docs to POST /orders
        {
          "order_id": 1001,
          "customer_id": 7,
          "amount": 49.99,
          "order_date": "2025-11-23T15:30:00"
        }


Scheduled ETL Integration
---------------------------------------

1. Make sure Redis is running.

2. Ensure the FastAPI app from Task 2 is running on port 8003:

    uvicorn backend.api.main:app --reload --port 8003
	
3. In another terminal, start Celery Beat:

	celery -A backend.api.schedule_etl beat --loglevel=info 
	
4. Start the Celery worker for the ETL app on a different terminal:

    celery -A backend.api.schedule_etl worker --loglevel=info -P solo
	

Log files are created in the current working directory when the ETL job runs.



Event-Driven Integration
-------------------------------------------------------

1. Ensure Redis is running.

2. Ensure the FastAPI app is running (Task 2):

    uvicorn backend.api.main:app --reload --port 8003

3. Start the Celery worker for the event integration:

    celery -A backend.api.event_intgrn worker --loglevel=info -P solo

4. Use the POST endpoint to create new orders. (/docs)

5. After each successful order creation, a new file will appear in:

    backend/api/order_events/

