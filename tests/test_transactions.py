from datetime import datetime

import pandas as pd
import pytest

from transactions import parse_transaction
from transactions import read_csv_transactions
from transactions import read_excel_transactions


def test_parse_transaction():
    """Проверка правильности конвертации типов"""
    test_row = {
        "id": "1",
        "state": "EXECUTED",
        "date": "2023-01-01T12:00:00Z",
        "amount": "100.5",
        "currency_name": "USD",
        "from": "Account 123",
        "to": "Account 456",
        "description": "Payment",
    }

    parsed = parse_transaction(test_row)

    assert parsed["amount"] == 100.5
    assert isinstance(parsed["date"], datetime)


def test_read_csv_transactions_success(tmp_path):
    """Проверка успешного чтения из csv"""
    csv_data = (
        "id;state;date;amount;currency_name;from;to;description\n"
        "1;EXECUTED;2023-01-01T12:00:00Z;100.5;USD;Account 123;Account 456;Payment"
    )
    file_path = tmp_path / "test.csv"
    file_path.write_text(csv_data, encoding="utf-8")

    transactions = read_csv_transactions(file_path)
    assert len(transactions) == 1
    assert transactions[0]["id"] == "1"


def test_read_csv_transactions_file_not_found():
    """Проверка на наличие файла по указанному пути"""
    with pytest.raises(FileNotFoundError):
        read_csv_transactions("notexist.csv")


def test_read_csv_empty_file(tmp_path):
    """Тест на пустой CSV файл"""
    file_path = tmp_path / "empty.csv"
    file_path.write_text("", encoding="utf-8")

    with pytest.raises(ValueError) as excinfo:
        read_csv_transactions(file_path)
    assert "CSV-файл пуст" in str(excinfo.value)


def test_read_excel_transactions_success(tmp_path):
    """Проверка успешного чтения excel файла"""
    data = {
        "id": [1],
        "state": ["EXECUTED"],
        "date": ["2023-01-01T12:00:00Z"],
        "amount": [100.5],
        "currency_name": ["USD"],
        "from": ["Account 123"],
        "to": ["Account 456"],
        "description": ["Payment"],
    }
    df = pd.DataFrame(data)
    file_path = tmp_path / "test.xlsx"
    df.to_excel(file_path, index=False)

    transactions = read_excel_transactions(file_path)
    assert len(transactions) == 1
    assert transactions[0]["id"] == 1


def test_read_excel_transactions_file_not_found():
    """Проверка на наличие файла по указанному пути"""
    with pytest.raises(FileNotFoundError):
        read_excel_transactions("notexist.xlsx")


def test_read_excel_empty_dataframe(tmp_path):
    """Тест на пустой DataFrame"""
    file_path = tmp_path / "empty_df.xlsx"
    pd.DataFrame().to_excel(file_path, index=False)

    with pytest.raises(ValueError, match="Excel-файл пуст"):
        read_excel_transactions(file_path)
