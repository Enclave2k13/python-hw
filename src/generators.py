def filter_by_currency(transactions, currency):
    """Возвращает итератор транзакций с заданной валютой."""
    return filter(lambda x: x["operationAmount"]["currency"]["code"] == currency, transactions)


def transaction_descriptions(transactions):
    """Генератор, который возвращает описание каждой транзакции по очереди."""
    return (transaction["description"] for transaction in transactions)


def card_number_generator(start, end):
    """Генератор, который генерирует номера карт в заданном диапазоне."""
    if start < 1 or end < 1:
        raise ValueError("Значения должны быть положительными")

    if start > 9999999999999999 or end > 9999999999999999:
        raise ValueError("Значения не могут превышать 9999999999999999")

    if start > end:
        return

    yield from (map(lambda x: " ".join([f"{x:016d}"[i : i + 4] for i in range(0, 16, 4)]), range(start, end + 1)))
