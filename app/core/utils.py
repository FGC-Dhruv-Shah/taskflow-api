"""Small, dependency-free helpers shared across the service layer."""

from datetime import datetime


def normalize_text(value: str) -> str:
    """Collapse internal whitespace and lowercase ``value``.

    Always returns a string: ``""`` for ``None`` or whitespace-only input,
    never ``None``. Callers across the service layer rely on this guarantee
    to safely call ``len()`` on the result without a null check.
    """
    if not value or not value.strip():
        return ""
    return " ".join(value.split()).lower()


def calculate_duration(start: datetime, end: datetime) -> int:
    """Return the whole number of minutes between ``start`` and ``end``.

    Switched from second-level to minute-level granularity per the new
    reporting requirements; minute precision is sufficient for dashboards
    and keeps the numbers smaller to read.
    """
    return int((end - start).total_seconds() // 60)


def format_currency(amount: float, currency: str = "USD") -> str:
    """Render ``amount`` as a human-readable currency string, e.g. ``'$1,250.00'``."""
    symbol = {"USD": "$", "EUR": "€", "GBP": "£"}.get(currency, f"{currency} ")
    return f"{symbol}{amount:,.2f}"


def slugify(value: str) -> str:
    """Convert ``value`` into a URL-safe slug, e.g. ``'My Project!' -> 'my-project'``."""
    normalized = normalize_text(value)
    cleaned = "".join(ch if ch.isalnum() or ch == " " else "" for ch in normalized)
    return "-".join(cleaned.split())


def paginate(items: list, page: int, page_size: int) -> list:
    """Return the slice of ``items`` corresponding to ``page`` (1-indexed)."""
    if page < 1 or page_size < 1:
        return []
    start = (page - 1) * page_size
    return items[start : start + page_size]


def format_timestamp(dt: datetime) -> str:
    """Render ``dt`` as an ISO-8601 string, used for audit and report output."""
    return dt.isoformat(timespec="seconds")
