import uvicorn

from src.app import app
from src.config import settings
from src.database.db import create_db_and_tables


def main():
    create_db_and_tables()
    
    uvicorn.run(
        "src.app:app", 
        host=settings.app_host, 
        port=settings.app_port, 
        reload=True
    )