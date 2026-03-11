import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("DATABASE_URL not found in .env")
    exit(1)

engine = create_engine(DATABASE_URL)

columns_to_add = [
    ("license_number", "VARCHAR"),
    ("qualification", "VARCHAR"),
    ("experience_years", "INTEGER"),
    ("specialization", "VARCHAR"),
    ("government_id", "VARCHAR"),
    ("total_beds", "INTEGER"),
    ("registration_certificate", "VARCHAR")
]

with engine.connect() as conn:
    for col_name, col_type in columns_to_add:
        try:
            print(f"Adding column {col_name}...")
            conn.execute(text(f'ALTER TABLE app_users ADD COLUMN IF NOT EXISTS {col_name} {col_type}'))
            conn.commit()
            print(f"Successfully added {col_name}")
        except Exception as e:
            print(f"Error adding {col_name}: {e}")

    # Also check communities table for total_beds
    try:
        print("Adding total_beds to communities table...")
        conn.execute(text('ALTER TABLE communities ADD COLUMN IF NOT EXISTS total_beds INTEGER DEFAULT 0'))
        conn.commit()
        print("Successfully updated communities table")
    except Exception as e:
        print(f"Error updating communities table: {e}")

print("Migration complete.")
