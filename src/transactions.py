import csv
import os
from datetime import datetime

import pandas as pd


def parse_transaction(row, source_format="default"):
    """Преобразует строки в соответствующие типы данных."""
    try:
        if source_format == "json":
            # Только для JSON - особый формат
            return {
                "id": row.get("id"),
                "date": datetime.fromisoformat(row["date"].replace("Z", "+00:00")),
                "amount": float(row["operationAmount"]["amount"]),
                "description": row["description"],
                "currency": row["operationAmount"]["currency"]["code"],
                "status": row.get("state", "UNKNOWN"),
                "from": row.get("from", ""),
                "to": row.get("to", ""),
            }
        else:
            # Для CSV и Excel - одинаковый простой формат
            return {
                "id": row.get("id"),
                "date": datetime.strptime(str(row["date"]), "%Y-%m-%dT%H:%M:%SZ"),
                "amount": float(row["amount"]),
                "description": row.get("description", ""),
                "currency": row.get("currency_code", "RUB"),
                "status": row.get("state", "UNKNOWN"),
                "from": row.get("from", ""),
                "to": row.get("to", ""),
            }

    except (ValueError, KeyError):
        return None


def read_csv_transactions(file_path):
    path = str(file_path)
    """Считывает транзакции из csv файла и возвращает список словарей с транзакциями"""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Файл не найден: {path}")
    if not path.lower().endswith(".csv"):
        raise ValueError("Файл должен быть в формате .csv")

    transactions = []
    try:
        with open(path, encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")
            if not reader.fieldnames:
                raise ValueError("CSV-файл пуст")
            for row in reader:
                parsed = parse_transaction(row)
                if parsed is not None:
                    transactions.append(parsed)
    except csv.Error as e:
        raise ValueError(f"Ошибка чтения CSV: {e}")

    if not transactions:
        raise ValueError("Файл не содержит транзакций")
    return transactions


def read_excel_transactions(file_path):
    """Считывает транзакции из excel файла и возвращает список словарей с транзакциями"""
    path = str(file_path)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Файл не найден: {path}")
    if not path.lower().endswith((".xlsx", ".xls")):
        raise ValueError("Файл должен быть в формате .xlsx или .xls")

    try:
        excel_data = pd.read_excel(path)
    except Exception as e:
        raise ValueError(f"Ошибка чтения Excel: {e}")
    if excel_data.empty:
        raise ValueError("Excel-файл пуст")

    # Получаем сырые данные
    raw_transactions = excel_data.to_dict(orient="records")
    if not raw_transactions:
        raise ValueError("Нет данных для обработки")

    # Парсим каждую транзакцию
    parsed_transactions = []
    for raw_row in raw_transactions:
        parsed = parse_transaction(raw_row)
        if parsed is not None:
            parsed_transactions.append(parsed)

    if not parsed_transactions:
        raise ValueError("Excel-файл не содержит валидных транзакций")

    return parsed_transactions
