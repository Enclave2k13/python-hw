from typing import Any
from typing import Dict
from typing import List

import pytest


@pytest.fixture
def sample_data() -> List[Dict[str, Any]]:
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-15T10:30:00"},
        {"id": 2, "state": "PENDING", "date": "2023-01-10T12:15:00"},
        {"id": 3, "state": "EXECUTED", "date": "2023-01-20T08:45:00"},
        {"id": 4, "state": "CANCELED", "date": "2023-01-05T14:20:00"},
        {"id": 5, "state": "EXECUTED", "date": "2023-01-20T08:45:00"},
    ]


@pytest.fixture
def empty_data() -> List[dict]:
    return []


@pytest.fixture
def invalid_date_data() -> List[Dict[str, Any]]:
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-15"},
        {"id": 2, "state": "EXECUTED", "date": "invalid-date"},
        {"id": 3, "state": "EXECUTED", "date": None},
    ]


@pytest.fixture
def sample_transactions():
    return [
        {
            "id": 1,
            "operationAmount": {"amount": "100.00", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
        },
        {
            "id": 2,
            "operationAmount": {"amount": "200.00", "currency": {"name": "Euro", "code": "EUR"}},
            "description": "Перевод со счета на счет",
        },
        {
            "id": 3,
            "operationAmount": {"amount": "300.00", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод с карты на карту",
        },
        {
            "id": 4,
            "operationAmount": {"amount": "400.00", "currency": {"name": "British Pound", "code": "GBP"}},
            "description": "",
        },
    ]


@pytest.fixture
def empty_transactions():
    """Фикстура с пустым списком транзакций"""
    return []


@pytest.fixture
def empty_description():
    """Фикстура транзакции с пустым полем description"""
    return [{"id": 1, "operationAmount": {"amount": "100.00", "currency": {"name": "USD", "code": "USD"}}}]
