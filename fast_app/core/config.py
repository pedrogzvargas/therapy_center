from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Therapy Center API"
    debug: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
