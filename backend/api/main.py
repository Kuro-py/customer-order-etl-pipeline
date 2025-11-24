from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import joinedload
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from backend.api.event_intgrn import order_created_event

from backend.database.db_models import Customer, Order
from backend.database.db_setup import SessionLocal

app = FastAPI(title="Customer & Orders API")


# Pydantic models used for data validation
class OrderSchema(BaseModel):
    order_id: int
    amount: float
    order_date: datetime
    model_config = {
        "from_attributes": True
    }


class CustomerSchema(BaseModel):
    customer_id: int
    firstname: str
    surname: str
    address: str
    status: str
    email: str
    zipcode: str
    region: str
    orders: List[OrderSchema] = []

    model_config = {
        "from_attributes": True
    }


class OrderCreateSchema(BaseModel):

    order_id: int
    customer_id: int
    amount: float
    order_date: datetime

@app.get("/")
def root():
    return {"message": "Landing API page"}

# First endpoint: return all customers with their orders (optionally filtered by status for TASK 3)
@app.get("/customers", response_model=List[CustomerSchema])
def get_customers(status: str | None = None):
    with SessionLocal() as session:
        query = session.query(Customer).options(joinedload(Customer.orders))
        if status:
            query = query.filter(Customer.status == status)

        return query.all()

# Second endpoint: Returning a single customer and their orders by customer_id
@app.get("/customers/{customer_id}", response_model=CustomerSchema)
def get_customer(customer_id: int):


    with SessionLocal() as session:
        customer = (
            session.query(Customer)
            .options(joinedload(Customer.orders))
            .filter(Customer.customer_id == customer_id)
            .first()
        )

        if not customer:
            raise HTTPException(404, "Customer not found")

        return customer

# Third endpoint: Creating a new order for an existing customer

@app.post("/orders")
def create_order(order: OrderCreateSchema):

    with SessionLocal() as session:


        customer = (
            session.query(Customer)
            .filter(Customer.customer_id == order.customer_id)
            .first()
        )
        if not customer:
            raise HTTPException(404, "Customer not found")

        existing_order = session.query(Order).filter(Order.order_id == order.order_id).first()

        if existing_order:
            raise HTTPException(400, "Order ID already exists")

        # Creating the new order
        new_order = Order(
            order_id=order.order_id,
            customer_id=order.customer_id,
            amount=order.amount,
            order_date=order.order_date
        )

        session.add(new_order)
        session.commit()

        # Sending "order created" event to the queue (used in Task 4 integration)

        order_created_event.delay({
            "order_id": new_order.order_id,
            "customer_id": new_order.customer_id,
            "amount": new_order.amount,
            "order_date": str(new_order.order_date)
        })
        return {
            "message": "Order created successfully",
            "order": {
                "order_id": new_order.order_id,
                "customer_id": new_order.customer_id,
                "amount": new_order.amount,
                "order_date": new_order.order_date
            }
        }

