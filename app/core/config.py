import os
from dotenv import load_dotenv

# Resolve .env path relative to this file and normalize it
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    # Fall back to default load (reads from current working dir or environment)
    load_dotenv()
    print(f"Warning: .env file not found at: {dotenv_path}; continuing with environment variables")


class Settings:
    PROJECT_NAME: str = "E-connect"
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    try:
        ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    except (TypeError, ValueError):
        ACCESS_TOKEN_EXPIRE_MINUTES = 30


settings = Settings()

# Basic validation for critical settings
if not settings.SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set. Please set SECRET_KEY in .env or environment variables.")
