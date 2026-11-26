"""Application configuration and runtime constants."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Immutable application settings loaded once at startup."""

    app_name: str = "TaskFlow API"
    api_version: str = "v1"
    default_page_size: int = 20
    max_page_size: int = 100
    default_currency: str = "USD"


settings = Settings()
