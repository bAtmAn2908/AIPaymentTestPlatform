import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "PaymentTestPlatform"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://payment_user:payment_password@localhost:5432/payment_test_db")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

settings = Settings()
