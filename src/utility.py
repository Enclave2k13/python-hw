from datetime import datetime


def convert_date(original_date):
    """Конвертирует ISO дату в формат YYYY-MM-DD."""
    dt = datetime.fromisoformat(original_date)
    return dt.strftime("%Y-%m-%d")
