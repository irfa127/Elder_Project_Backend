import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

columns_to_add = [
    ("dob", "VARCHAR"),
    ("gender", "VARCHAR"),
    ("blood_group", "VARCHAR"),
    ("emergency_contact_name", "VARCHAR"),
    ("emergency_contact_phone", "VARCHAR"),
    ("medical_condition", "TEXT"),
    ("mobility_status", "VARCHAR")
]

with engine.connect() as conn:
    for col_name, col_type in columns_to_add:
        try:
            print(f"Adding column {col_name} to app_users...")
            conn.execute(text(f'ALTER TABLE app_users ADD COLUMN IF NOT EXISTS {col_name} {col_type}'))
            conn.commit()
            print(f"Successfully added {col_name}")
        except Exception as e:
            print(f"Error adding {col_name}: {e}")

print("Migration v3 complete.")
