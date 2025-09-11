import pytest

from src.widget import get_date
from src.widget import mask_account_card


# Позитивные тесты для карт
@pytest.mark.parametrize(
    "input_data, expected",
    [
        ("Visa Platinum 7000792289606361", "7000 79** **** 6361"),
        ("Maestro 1234567812345678", "1234 56** **** 5678"),
        ("МИР 0000000000000000", "0000 00** **** 0000"),
        ("MasterCard 9999888877776666", "9999 88** **** 6666"),
    ],
)
def test_card_masking_positive(input_data: str, expected: str) -> None:
    """Проверяем корректное маскирование разных типов карт"""
    assert mask_account_card(input_data) == expected


# Позитивные тесты для счетов
@pytest.mark.parametrize(
    "input_data, expected",
    [
        ("Счет 73654108430135874305", "**4305"),
        ("Счет 12345678901234567890", "**7890"),
        ("Счет 00000000000000000001", "**0001"),
    ],
)
def test_account_masking_positive(input_data: str, expected: str) -> None:
    """Проверяем корректное маскирование разных форматов счетов"""
    assert mask_account_card(input_data) == expected


# Негативные тесты для карт
@pytest.mark.parametrize(
    "invalid_input",
    [
        "Visa 70007",  # Слишком короткий
        "Maestro abcdefghijklmnop",  # Буквы
        "МИР 123456781234567890",  # Слишком длинный
    ],
)
def test_card_masking_errors(invalid_input: str) -> None:
    """Проверяем, что невалидные входные данные вызывают ValueError"""
    with pytest.raises(ValueError):
        mask_account_card(invalid_input)


# Негативные тесты для счетов
@pytest.mark.parametrize(
    "invalid_input",
    [
        "Счет 7365",  # Слишком короткий номер
        "Счет abcdef",  # Некорректные символы (буквы)
        "Счет ",  # Пустой номер счета
    ],
)
def test_account_masking_errors(invalid_input: str) -> None:
    """Проверяем, что невалидные номера счетов вызывают ValueError"""
    with pytest.raises(ValueError):
        mask_account_card(invalid_input)


@pytest.mark.parametrize(
    "invalid_input, expected_error",
    [
        ("Счет", "Строка не содержит нужной информации для обработки"),
        ("Visa", "Строка не содержит нужной информации для обработки"),
        ("Mastercard", "Строка не содержит нужной информации для обработки"),
        ("Счет ", "Строка не содержит нужной информации для обработки"),
    ],
)
def test_mask_account_card_errors(invalid_input: str, expected_error: str) -> None:
    with pytest.raises(ValueError) as exc_info:
        mask_account_card(invalid_input)
    assert expected_error in str(exc_info.value)


# Тест для стандартных форматов дат
@pytest.mark.parametrize(
    "input_date, expected",
    [
        ("2023-12-31", "31.12.2023"),
        ("2020-02-29", "29.02.2020"),
        ("1999-01-01", "01.01.1999"),
        ("2000-12-31T23:59:59", "31.12.2000"),
        ("2023-06-15T00:00:00Z", "15.06.2023"),
    ],
)
def test_standard_date_formats(input_date: str, expected: str) -> None:
    """Проверяем корректное преобразование стандартных форматов дат"""
    assert get_date(input_date) == expected


# Тест для нестандартных форматов дат
@pytest.mark.parametrize(
    "input_date, expected",
    [
        ("2023/12/31", "31.12.2023"),  # Разные разделители
        ("31-12-2023", "31.12.2023"),  # Обратный порядок
        ("Dec 31 2023", "31.12.2023"),  # Текстовая дата (сокр.)
        ("15 June 2023", "15.06.2023"),  # Текстовая дата (полн.)
        ("2023.06.15", "15.06.2023"),  # С точками как разделителями
    ],
)
def test_non_standard_formats(input_date: str, expected: str) -> None:
    """Проверяем обработку нестандартных форматов даты"""
    assert get_date(input_date) == expected


# Тест для граничных случаев
@pytest.mark.parametrize(
    "input_date, expected",
    [
        ("0001-01-01", "01.01.0001"),  # Минимальная дата
        ("9999-12-31", "31.12.9999"),  # Максимальная дата
        ("1970-01-01", "01.01.1970"),  # Unix epoch
    ],
)
def test_edge_cases(input_date: str, expected: str) -> None:
    """Проверяем обработку граничных случаев"""
    assert get_date(input_date) == expected


# Тест для некорректных данных
@pytest.mark.parametrize(
    "invalid_input",
    [
        "",  # Пустая строка
        "not a date",  # Текст вместо даты
        "123456",  # Число
        "2023-13-01",  # Несуществующий месяц
        "2023-02-30",  # Несуществующая дата
        None,  # None
    ],
)
def test_invalid_input(invalid_input: str) -> None:
    """Проверяем обработку некорректных входных данных"""
    with pytest.raises((ValueError, TypeError)):
        get_date(invalid_input)
