from typing import Any
from typing import Dict
from typing import List

import pytest

from src.processing import filter_by_state
from src.processing import sort_by_date


@pytest.mark.parametrize(
    "state, expected_ids",
    [
        ("EXECUTED", [1, 3, 5]),
        ("PENDING", [2]),
        ("CANCELED", [4]),
        ("UNKNOWN", []),
    ],
)
def test_filter_by_state(sample_data: List[Dict[str, Any]], state: str, expected_ids: List[int]) -> None:
    """Тестируем фильтрацию по разным состояниям"""
    result = filter_by_state(sample_data, state)
    assert [item["id"] for item in result] == expected_ids


def test_filter_empty_data(empty_data: List[dict]) -> None:
    """Тестируем фильтрацию пустого списка"""
    assert filter_by_state(empty_data) == []


def test_filter_default_state(sample_data: List[Dict[str, Any]]) -> None:
    """Тестируем фильтрацию со значением state по умолчанию"""
    result = filter_by_state(sample_data)
    assert all(item["state"] == "EXECUTED" for item in result)


@pytest.mark.parametrize(
    "reverse, expected_order",
    [
        (True, [3, 5, 1, 2, 4]),  # По убыванию (по умолчанию)
        (False, [4, 2, 1, 3, 5]),  # По возрастанию
    ],
)
def test_sort_by_date(sample_data: List[Dict[str, Any]], reverse: bool, expected_order: List[int]) -> None:
    """Тестируем сортировку по дате"""
    result = sort_by_date(sample_data, reverse)
    assert [item["id"] for item in result] == expected_order


def test_sort_with_equal_dates(sample_data: List[Dict[str, Any]]) -> None:
    """Тестируем сортировку с одинаковыми датами"""
    result = sort_by_date(sample_data)
    # Проверяем что записи с одинаковой датой (id 3 и 5) сохраняют исходный порядок
    assert result[0]["id"] == 3
    assert result[1]["id"] == 5


def test_sort_empty_data(empty_data: List[dict]) -> None:
    """Тестируем сортировку пустого списка"""
    assert sort_by_date(empty_data) == []


def test_sort_invalid_dates(invalid_date_data: List[Dict[str, Any]]) -> None:
    """Тестируем сортировку с некорректными датами"""
    with pytest.raises((ValueError, TypeError)):
        sort_by_date(invalid_date_data)
