"""Application settings. The only place that reads environment variables."""

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

Provider = Literal["router", "vertex"]  # Langflow flow variant


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=("../.env", ".env"),
        extra="ignore",
        case_sensitive=False,
    )

    # General
    app_env: str = "local"
    log_level: str = "INFO"
    cors_origins: str = "http://localhost:3000"
    seed_dir: str = "../data/seed"

    # Database
    database_url: str = "postgresql+psycopg://learnfl0w:learnfl0w@localhost:5432/learnfl0w"

    # Auth
    jwt_secret: str = "change-me-change-me-change-me-change-me"
    jwt_access_ttl_minutes: int = 30
    refresh_ttl_days: int = 7
    admin_emails: str = ""
    login_max_attempts: int = 5
    login_window_minutes: int = 15

    # AI layer (Langflow). The backend never calls an LLM directly.
    llm_provider: Provider = "router"
    llm_fallback_provider: Provider = "vertex"
    langflow_base_url: str = "http://localhost:7860"
    langflow_api_key: str = ""
    langflow_use_id_token: bool = False
    langflow_timeout_seconds: int = 30
    langflow_roadmap_timeout_seconds: int = 60
    llm_circuit_failure_threshold: int = 3
    llm_circuit_reset_seconds: int = 60
    internal_tool_token: str = ""

    # Embedding (called from the backend)
    vertex_project: str = ""
    vertex_location: str = "asia-southeast2"
    embedding_provider: Literal["vertex", "onnx"] = "vertex"
    embedding_model: str = ""

    # Limits
    daily_session_limit: int = 5
    max_turns_per_session: int = 25

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def admin_email_set(self) -> set[str]:
        return {e.strip().lower() for e in self.admin_emails.split(",") if e.strip()}


@lru_cache
def get_settings() -> Settings:
    return Settings()
