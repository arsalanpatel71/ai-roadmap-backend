from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    MONGO_URI: str

    OPENAI_API_KEY: str
    ASSISTANT_ID: str

    CORS_ORIGINS: List[str] = ["*"] 

    SENDGRID_API_KEY: str
    FROM_EMAIL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings() 