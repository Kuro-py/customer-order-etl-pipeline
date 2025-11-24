from backend.database.db_setup import engine, Base
from backend.database.db_models import Customer, Order

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database initialised and tables created")


if __name__ == "__main__":
    init_db()
