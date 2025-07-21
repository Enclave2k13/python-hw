import pytest
from src.utility import convert_date


@pytest.mark.parametrize(
    "input_date, expected_output",
    [
        ("2024-07-21T15:30:45", "2024-07-21"),
        ("2023-01-01T00:00:00", "2023-01-01"),
        ("2019-08-26T10:50:58.294041", "2019-08-26"),
    ],
)
def test_convert_date_valid(input_date, expected_output):
    """Проверяет, что ISO дата корректно обрезается до YYYY-MM-DD"""
    assert convert_date(input_date) == expected_output


def test_convert_date_invalid_format():
    """Выбрасывает ошибку при неправильном формате"""
    with pytest.raises(ValueError):
        convert_date("21-07-2024")
