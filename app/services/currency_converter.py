"""Static-rate currency conversion for budget reporting."""

import logging

logger = logging.getLogger(__name__)

_RATES_TO_USD = {"USD": 1.0, "EUR": 1.08, "GBP": 1.27}


class CurrencyConverter:
    """Converts an amount from one supported currency to another."""

    def convert(self, amount: float, from_currency: str, to_currency: str) -> dict:
        """Convert ``amount`` from ``from_currency`` to ``to_currency``."""
        usd = amount * _RATES_TO_USD.get(from_currency, 1.0)
        converted = usd / _RATES_TO_USD.get(to_currency, 1.0)
        return {"amount": round(converted, 2), "currency": to_currency}

    def supports(self, currency: str) -> bool:
        return currency in _RATES_TO_USD
