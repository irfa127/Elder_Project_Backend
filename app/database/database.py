from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from app.core.config import settings


db_url = settings.DATABASE_URL
if not db_url:
    
    print("Warning: DATABASE_URL not found in settings.")
    db_url = "sqlite:///./test.db"

engine = create_engine(db_url)
Base = declarative_base()
