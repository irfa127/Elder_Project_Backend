import os
from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
inspector = inspect(engine)

print("Tables in database:")
for table_name in inspector.get_table_names():
    print(f"\nTable: {table_name}")
    for column in inspector.get_columns(table_name):
        print(f"  Column: {column['name']} ({column['type']})")

print("\nVerification complete.")
