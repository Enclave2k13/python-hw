import json

from log_config import setup_logger

from .external_api import convert_amount

logger = setup_logger("utils", "utils.log")


def retrieve_transactions_by_path(path):
    """Читает JSON-файл по указанному пути и возвращает список транзакций.
     Если файл не найден, пустой, содержит некорректный JSON или JSON не является списком,
    возвращает пустой список."""
    try:
        logger.debug(f"Начало обработки файла: {path}")

        with open(path, encoding="utf-8") as f:
            data = json.load(f)
            result = data if isinstance(data, list) else []
            logger.info(f"Успешно прочитано {len(result)} транзакций")
            return result
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
