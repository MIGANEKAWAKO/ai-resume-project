import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    deepseek_api_key: str = os.getenv("DEEPSEEK_API_KEY", "sk-placeholder")
    deepseek_base_url: str = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    deepseek_model: str = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

    database_url: str = os.getenv(
        "DATABASE_URL",
        "sqlite+aiosqlite:///./resume.db",
    )

    max_upload_size_mb: int = 10
    upload_dir: str = os.getenv("UPLOAD_DIR", "./uploads")

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
