import os
from pydantic import BaseConfig

class Settings:
    PROJECT_NAME: str = "Fashion E-Commerce Store"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Secret Key for JWT Authentication
    SECRET_KEY: str = os.getenv("SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # Database Settings - Default to MySQL, fallback to SQLite if MySQL fails or SQLite selected
    MYSQL_USER: str = os.getenv("MYSQL_USER", "fashion_user")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "your_password")
    MYSQL_HOST: str = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT: str = os.getenv("MYSQL_PORT", "3306")
    MYSQL_DB: str = os.getenv("MYSQL_DB", "fashion_db")

    @property
    def DATABASE_URL(self) -> str:
        env_url = os.getenv("DATABASE_URL")
        if env_url:
            return env_url
        return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}"

    @property
    def FALLBACK_SQLITE_URL(self) -> str:
        return "sqlite:///./fashion.db"

settings = Settings()
