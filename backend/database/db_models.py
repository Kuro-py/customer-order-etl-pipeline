from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from backend.database.db_setup import Base

# SQLAlchemy ORM models representing the database tables used in SQLite.


# Customer table definition
class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    address = Column(String, nullable=False)
    email = Column(String, nullable=False)
    zipcode = Column(String, nullable=True)
    region = Column(String, nullable=False)
    status = Column(String, nullable=False)


    orders = relationship("Order", back_populates="customer", cascade="all, delete-orphan")


# Order table definition

class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, autoincrement=False)
    order_date = Column(DateTime, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False)
    amount = Column(Float, nullable=False)

    customer = relationship("Customer", back_populates="orders")
