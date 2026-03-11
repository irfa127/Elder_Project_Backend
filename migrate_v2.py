import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    try:
        print("Adding registration_id to communities table...")
        conn.execute(text('ALTER TABLE communities ADD COLUMN IF NOT EXISTS registration_id VARCHAR'))
        conn.commit()
        print("Successfully updated communities table")
    except Exception as e:
        print(f"Error updating communities table: {e}")

print("Migration complete.")
