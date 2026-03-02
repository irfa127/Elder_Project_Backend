# ElderConnect Backend

## Structure
- `app/`: Main FastAPI application
  - `core/`: Configuration and security
  - `database/`: DB engine and session
  - `models/`: SQLAlchemy models
  - `schemas/`: Pydantic schemas
  - `routers/`: API endpoints
- `scripts/`: Utility scripts (init db, seed data, etc.)
- `venv/`: Python virtual environment
- `.env`: Environment variables

## Setup
1. Activate virtual environment:
   ```bash
   # Windows
   .\venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Initialize Database:
   ```bash
   python scripts/init_db.py
   python scripts/seed_data.py
   ```
4. Run the server:
   ```bash
   python -m uvicorn app.main:app --reload

   ```

## API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

run the Script and Server 
