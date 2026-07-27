from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.3-70b-versatile"  # active model on Groq
    
    # Project root is two levels up from backend/app/config.py
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    OUTPUT_DIR: Path = Path(__file__).resolve().parent.parent.parent / "outputs"
    
    CORS_ORIGINS: List[str] = ["*"]
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

# Ensure output directories exist
(settings.OUTPUT_DIR / "stories").mkdir(parents=True, exist_ok=True)
(settings.OUTPUT_DIR / "audio").mkdir(parents=True, exist_ok=True)
