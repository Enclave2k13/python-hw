import os
import sys
from pathlib import Path

from decorators import log
from src.generators import filter_by_currency
from src.processing import filter_by_state
from src.processing import sort_by_date
from src.transactions import read_csv_transactions
from src.transactions import read_excel_transactions
from src.utils import process_bank_search
from src.utils import retrieve_transactions_by_path
from src.widget import mask_account_card

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@log()
def main():
    greeting = "Привет! Добро пожаловать в программу работы с банковскими транзакциями."
    print(greeting)

    file_type = get_file_type()

    PROJECT_DIR = Path(__file__).parent.parent
    DATA_DIR = PROJECT_DIR / "data"

    file_handlers = {
        "JSON": {"path": DATA_DIR / "operations.json", "reader": retrieve_transactions_by_path},
        "CSV": {"path": DATA_DIR / "transactions.csv", "reader": read_csv_transactions},
        "XLSX": {"path": DATA_DIR / "transactions_excel.xlsx", "reader": read_excel_transactions},
    }

    handler = file_handlers[file_type]
    file_path = handler["path"]
    reader_func = handler["reader"]

    transactions = reader_func(file_path)
    status = get_transaction_status()
    filtered_transactions = filter_by_state(transactions, status)

    if confirm_action("\nОтсортировать операции по дате?"):
        direction = get_sort_direction()
        is_reverse = direction == "desc"
        filtered_transactions = sort_by_date(filtered_transactions, is_reverse)

    if confirm_action("Выводить только рублевые транзакции?"):
        filtered_transactions = filter_by_currency(filtered_transactions, "RUB")

    if confirm_action("Отфильтровать список транзакций по определенному слову в описании?"):
        keyword = input("Введите ключевое слово для фильтрации: ").strip()
        filtered_transactions = process_bank_search(filtered_transactions, keyword)

    filtered_transactions = [t for t in filtered_transactions if t is not None]
    if not filtered_transactions:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        print("\nРаспечатываю итоговый список транзакций...\n")
        print_transactions(filtered_transactions)


@log(filename="mylog.txt")
def get_file_type() -> str:
    """Обрабатывает ответ пользователя и возвращает тип файла"""
    menu = """\nВыберите необходимый пункт меню:
    1. Получить информацию о транзакциях из JSON-файла
    2. Получить информацию о транзакциях из CSV-файла
    3. Получить информацию о транзакциях из XLSX-файла"""
    file_type = ""
    while True:
        try:
            choice = int(input(menu + "\n\nВаш выбор: "))
            if choice == 1:
                file_type = "JSON"
                break
            elif choice == 2:
                file_type = "CSV"
                break
            elif choice == 3:
                file_type = "XLSX"
                break
            else:
                print("Пожалуйста, введите число от 1 до 3\n")
        except ValueError:
            print("Пожалуйста, введите число\n")
    print(f"\nДля обработки выбран {file_type}-файл.")
    return file_type


@log()
def get_transaction_status() -> str:
    """Получает и возвращает статус транзакции"""
    question = """\nВведите статус, по которому необходимо выполнить фильтрацию.
Доступные для фильтрации статусы: EXECUTED, CANCELED, PENDING"""
    valid_statuses = {"executed", "canceled", "pending"}

    while True:
        user_choice = input(question + "\n\nВаш выбор: ").strip().lower()
        if user_choice in valid_statuses:
            status = user_choice.upper()
            print(f'Операции отфильтрованы по статусу "{status}"')
            return status
        print(f'Статус операции "{user_choice}" недоступен.\n')


@log(filename="mylog.txt")
def confirm_action(question: str) -> bool:
    """Запрашивает у пользователя ответ Да/Нет и возвращает булево значение"""
    while True:
        user_input = input(f"{question} (Да/Нет): ").strip().lower()

        if user_input in {"да"}:
            return True
        elif user_input in {"нет"}:
            return False
        else:
            print('Пожалуйста, ответьте "Да" или "Нет"\n')


@log()
def get_sort_direction() -> str:
    """Возвращает направление сортировки: 'asc' или 'desc'"""
    while True:
        direction = input("Отсортировать по возрастанию или по убыванию?").lower()
        if direction in {"по возрастанию", "в"}:
            return "asc"
        elif direction in {"по убыванию", "у"}:
            return "desc"
        print('Пожалуйста, укажите "по возрастанию" или "по убыванию"\n')


@log(filename="mylog.txt")
def print_transactions(transactions: list[dict]):
    """Выводит список транзакций"""
    if not transactions:
        print("Нет транзакций для отображения")
        return

    for i, transaction in enumerate(filter(None, transactions), 1):
        try:
            id = transaction["id"]
            date = transaction.get("date", "Дата неизвестна")
            description = transaction.get("description", "Без описания")
            amount = transaction.get("amount", 0.0)
            currency = transaction.get("currency", "RUB")

            print(f"\n{i}. {id} {date} {description}")

            if "from" in transaction and "to" in transaction:
                print(f"{mask_account_card(transaction['from'])} -> {mask_account_card(transaction['to'])}")
            elif "from" in transaction:
                print(f"Списание с {mask_account_card(transaction['from'])}")
            elif "to" in transaction:
                print(f"Зачисление на {mask_account_card(transaction['to'])}")

            print(f"Сумма: {amount:.2f} {currency}")
            print("-" * 50)

        except AttributeError as e:
            print(f"Ошибка форматирования транзакции: {e}")
            continue


if __name__ == "__main__":
    main()
