"""Application configuration and runtime constants."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Settings:
    """Immutable application settings loaded once at startup.

    The budget/alerting fields below back the project budget-alert feature:
    a project's utilization is compared against ``default_alert_threshold``
    (a project may override this per-project), conversions are limited to
    ``supported_currencies``, and repeat alerts for the same project are
    suppressed for ``alert_cooldown_hours``.
    """

    app_name: str = "TaskFlow API"
    api_version: str = "v1"
    default_page_size: int = 20
    max_page_size: int = 100
    default_currency: str = "USD"
    default_alert_threshold: float = 0.9
    supported_currencies: tuple = field(default_factory=lambda: ("USD", "EUR", "GBP"))
    alert_cooldown_hours: int = 24
    reminder_lookahead_hours: int = 48
    audit_retention_days: int = 90


settings = Settings()
