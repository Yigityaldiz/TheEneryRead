from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    OPENAI_API_KEY: str
    SECRET_KEY: str = "supersecretkey"
    
    # Abysis API
    ABYSIS_API_URL: str
    ABYSIS_USERNAME: str
    ABYSIS_PASSWORD: str
    ABYSIS_DEPARTMENT_CODE: str | None = None
    ABYSIS_API_KEY: str | None = None

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
