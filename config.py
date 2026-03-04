from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    database_url: str = "sqlite:///./coursework1.db"

    model_config = ConfigDict(env_file=".env")

settings = Settings()