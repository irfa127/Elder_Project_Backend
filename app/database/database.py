from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from app.core.config import settings


db_url = settings.DATABASE_URL

if not db_url:
    raise ValueError("DATABASE_URL is not set in environment variables")

engine = create_engine(db_url)
Base = declarative_base()
