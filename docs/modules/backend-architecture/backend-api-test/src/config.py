import os
from dataclasses import dataclass


@dataclass
class Settings:
    database_url: str = os.getenv("DATABASE_URL", "postgresql+psycopg://app:app@localhost:5432/app")
    jwt_secret: str = os.getenv("JWT_SECRET", "devsecret")
    jwt_alg: str = os.getenv("JWT_ALG", "HS256")


settings = Settings()

