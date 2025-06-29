import pytest

from src.generators import card_number_generator
from src.generators import filter_by_currency
from src.generators import transaction_descriptions


def test_filter_by_currency_success(sample_transactions):
    """Тест корректной фильтрации транзакций по валюте."""
    filtered = filter_by_currency(sample_transactions, "USD")
    result = list(filtered)

    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 3


def test_filter_by_currency_no_matches(sample_transactions):
    """Тест случая, когда нет транзакций в заданной валюте."""
    filtered = filter_by_currency(sample_transactions, "AAA")
    result = list(filtered)

    assert len(result) == 0


def test_filter_by_currency_empty_list():
    """Тест обработки пустого списка транзакций."""
    filtered = filter_by_currency([], "USD")
    result = list(filtered)

    assert len(result) == 0


def test_returns_correct_descriptions(sample_transactions):
    """Тест корректного возврата описаний"""
    gen = transaction_descriptions(sample_transactions)
    descriptions = list(gen)

    assert descriptions == ["Перевод организации", "Перевод со счета на счет", "Перевод с карты на карту", ""]


def test_empty_list_handling(empty_transactions):
    """Тест обработки пустого списка транзакций"""
    gen = transaction_descriptions(empty_transactions)
    descriptions = list(gen)

    assert descriptions == []


def test_missing_description_field(empty_description):
    """Тест обработки транзакции без поля description"""
    gen = transaction_descriptions(empty_description)

    with pytest.raises(KeyError):
        list(gen)


def test_generates_correct_sequence():
    """Тест генерации последовательности номеров карт"""
    generator = card_number_generator(1, 5)
    result = list(generator)

    assert result == [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005",
    ]


def test_format_correctness():
    """Тест корректности форматирования номеров карт"""
    generator = card_number_generator(1234567812345678, 1234567812345678)
    result = next(generator)

    assert result == "1234 5678 1234 5678"
    assert len(result) == 19  # 16 цифр + 3 пробела
    assert result.count(" ") == 3


def test_edge_cases():
    """Тест обработки крайних значений диапазона"""
    # Минимальное значение
    gen_min = card_number_generator(1, 1)
    assert next(gen_min) == "0000 0000 0000 0001"

    # Максимальное значение
    gen_max = card_number_generator(9999999999999999, 9999999999999999)
    assert next(gen_max) == "9999 9999 9999 9999"

    # Большой диапазон
    gen_large = card_number_generator(1, 100)
    assert len(list(gen_large)) == 100


def test_empty_range():
    """Тест обработки пустого диапазона (start > end)"""
    generator = card_number_generator(10, 5)
    result = list(generator)

    assert result == []


def test_invalid_values():
    """Тест обработки недопустимых значений"""
    with pytest.raises(ValueError):
        # Отрицательные значения
        list(card_number_generator(-1, 5))

    with pytest.raises(ValueError):
        # Слишком большие значения
        list(card_number_generator(1, 10000000000000000))
