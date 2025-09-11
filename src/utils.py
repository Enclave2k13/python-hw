import json
import re
from collections import Counter

from log_config import setup_logger
from src.external_api import convert_amount
from transactions import parse_transaction

logger = setup_logger("utils", "utils.log")


def retrieve_transactions_by_path(path):
    """Читает JSON-файл по указанному пути и возвращает список транзакций.
     Если файл не найден, пустой, содержит некорректный JSON или JSON не является списком,
    возвращает пустой список."""
    try:
        logger.debug(f"Начало обработки файла: {path}")

        with open(path, encoding="utf-8") as f:
            data = json.load(f)
            transactions = []
            for item in data:
                parsed = parse_transaction(item, "json")
                if parsed is not None:
                    transactions.append(parsed)
            logger.info(f"Успешно прочитано {len(transactions)} транзакций")
            return transactions
    except FileNotFoundError:
        logger.error(f"Файл не найден: {path}")
        return []
    except json.JSONDecodeError:
        logger.error(f"Ошибка формата JSON в файле: {path}")
        return []
    except Exception as e:
        logger.exception(f"Неизвестная ошибка при чтении файла: {e}")
        return []


def retrieve_transaction_amount(transaction):
    """Возвращает сумму транзакции в рублях (float).
    Если валюта транзакции — не RUB (например, USD или EUR), то
    конвертирует её через API (external_api.convert_amount)."""
    try:
        logger.debug(f"Начало обработки транзакции: {transaction}")

        if not isinstance(transaction, dict):
            logger.warning("Транзакция не является словарем")
            return 0.0

        amount = transaction.get("operationAmount", {}).get("amount")
        currency_code = transaction.get("operationAmount", {}).get("currency").get("code")

        if currency_code == "RUB":
            logger.debug(f"Найдена сумма в RUB: {amount}")
            return amount

        logger.debug(f"Начало конвертации {amount} {currency_code} в RUB")
        converted = convert_amount(amount, currency_code, "RUB", transaction.get("date"))
        logger.info(f"Успешная конвертация: {amount} {currency_code} → {converted} RUB")
        return converted
    except Exception as e:
        logger.error(f"Ошибка обработки транзакции: {str(e)}")
        return 0.0


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """Фильтрует транзакции по вхождению строки в описание"""
    if not search:
        return data
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    matched_transactions = []
    for transaction in data:
        if "description" in transaction:
            description = transaction["description"]
            if pattern.search(description):
                matched_transactions.append(transaction)
    return matched_transactions


def process_bank_operations(data: list[dict], categories: list) -> dict:
    """Подсчитывает количество операций по заданным категориям."""
    categories_lower = [cat.lower() for cat in categories]
    descriptions = [transaction.get("description", "").lower() for transaction in data]

    description_counts = Counter(descriptions)

    result = {}
    for category, category_lower in zip(categories, categories_lower):
        result[category] = description_counts.get(category_lower, 0)

    return result
