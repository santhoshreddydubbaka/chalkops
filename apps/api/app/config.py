from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path
import os

# apps/api/.env (config.py lives in apps/api/app/config.py)
ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=True)

class Settings(BaseModel):
    database_url: str | None = os.getenv("DATABASE_URL")

settings = Settings()
