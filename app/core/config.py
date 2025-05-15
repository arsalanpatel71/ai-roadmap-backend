from pydantic_settings import BaseSettings
from typing import List
import json

class Settings(BaseSettings):
    MONGO_URI: str

    OPENAI_API_KEY: str
    ASSISTANT_ID: str

    CORS_ORIGINS: List[str] = ["*"]  # Default to allow all origins

    SENDGRID_API_KEY: str
    FROM_EMAIL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str):
            if field_name == "CORS_ORIGINS" and isinstance(raw_val, str):
                try:
                    return json.loads(raw_val)
                except json.JSONDecodeError:
                    return raw_val.split(",")
            return raw_val

settings = Settings() 