import json

from .external_api import convert_amount


def retrieve_transactions_by_path(path):
    """Читает JSON-файл по указанному пути и возвращает список транзакций.
     Если файл не найден, пустой, содержит некорректный JSON или JSON не является списком,
    возвращает пустой список."""
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    return data if isinstance(data, list) and all(isinstance(item, dict) for item in data) else []


def retrieve_transaction_amount(transaction):
    """Возвращает сумму транзакции в рублях (float).
    Если валюта транзакции — не RUB (например, USD или EUR), то
    конвертирует её через API (external_api.convert_amount)."""
    if not isinstance(transaction, dict):
        return 0.0

    amount = transaction.get("operationAmount", {}).get("amount")
    currency_code = transaction.get("operationAmount", {}).get("currency").get("code")

    if currency_code == "RUB":
        return amount

    try:
        return convert_amount(amount, currency_code, "RUB", transaction.get("date"))
    except Exception:
        return 0.0
