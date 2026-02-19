from pydantic import BaseModel
import os

class Settings(BaseModel):
    database_url: str | None = os.getenv("DATABASE_URL")

settings = Settings()
