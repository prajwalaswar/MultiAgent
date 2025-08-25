from functools import lru_cache
from pathlib import Path
from typing import Dict, List
from pydantic import Field
from pydantic_settings import BaseSettings

# Try backend/.env first, then project-root/.env
_BASE = Path(__file__).resolve()
_CANDIDATES = [
    _BASE.parents[2] / ".env",  # backend/.env
    _BASE.parents[3] / ".env",  # project root .env
]
for p in _CANDIDATES:
    if p.exists():
        ENV_FILE = str(p)
        break
else:
    ENV_FILE = ".env"


class Settings(BaseSettings):
    app_name: str = "LangGraph AI Agent"
    version: str = "0.1.0"
    environment: str = Field(default="development")

    # API keys (read automatically from environment/.env)
    groq_api_key: str | None = Field(default=None, alias="GROQ_API_KEY")
    tavily_api_key: str | None = Field(default=None, alias="TAVILY_API_KEY")
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")

    # Server
    host: str = "127.0.0.1"
    port: int = 9999

    # Model registry
    models_by_provider: Dict[str, List[str]] = {
        "Groq": ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"],
        "OpenAI": ["gpt-4o-mini"],
    }

    class Config:
        env_file = ENV_FILE
        case_sensitive = False


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
