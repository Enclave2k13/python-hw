import csv
import os
from datetime import datetime

import pandas as pd


def parse_transaction(row):
    """Преобразует строки в соответствующие типы данных."""
    try:
        row["amount"] = float(row["amount"])  # или int, если amount всегда целое число
        row["date"] = datetime.strptime(row["date"], "%Y-%m-%dT%H:%M:%SZ")
    except (ValueError, KeyError) as e:
        raise ValueError(f"Ошибка парсинга транзакции: {e}. Данные: {row}") from e
    return row


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
                transactions.append(parse_transaction(row))
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

    transactions = excel_data.to_dict(orient="records")
    if not transactions:
        raise ValueError("Нет данных для обработки")
    return transactions
