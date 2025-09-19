from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import settings
from src.database.base import Base
# Import all the models, so they are registered with SQLAlchemy's metadata
from src.database.models import User, Book, BorrowedBook, CustomerRequest

db_url = f"mysql+pymysql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_database}"
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_db_and_tables():
    """
    Creates the database and all the tables defined in the models.
    """
    print("INFO:     Creating database and tables...")
    try:
        # Import all the models so they are registered with SQLAlchemy's metadata
        Base.metadata.create_all(bind=engine)
        print("INFO:     Database and tables created successfully.")
    except Exception as e:
        print(f"ERROR:    An error occurred while creating tables: {e}")
