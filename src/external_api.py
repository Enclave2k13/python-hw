import os

import requests

from .utility import convert_date


def convert_amount(amount, from_currency, to_currency, date=None):
    """Конвертирует сумму из одной валюты в другую."""
    API_KEY = os.getenv("API_KEY")
    url = "https://api.apilayer.com/currency_data/convert"
    params = {
        "amount": amount,
        "from": from_currency,
        "to": to_currency,
    }
    if date:
        params["date"] = convert_date(date)
    headers = {"apikey": API_KEY}

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    data = response.json()

    if not data.get("success", False):
        error_info = data.get("error", {}).get("info", "Неизвестная ошибка API")
        raise RuntimeError(f"Ошибка конвертации: {error_info}")
    try:
        return float(data["result"])
    except (TypeError, ValueError):
        raise RuntimeError("Некорректный результат конвертации")
