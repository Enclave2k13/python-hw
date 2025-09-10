def filter_by_state(data: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Функция фильтрует словари по заданному ключу state"""
    filtered_data = []
    for user_dict in data:
        if user_dict.get("status") == state:
            filtered_data.append(user_dict)
    return filtered_data


def sort_by_date(data: list[dict], is_reverse: bool = True) -> list[dict]:
    """Сортирует список словарей по дате (по умолчанию — по убыванию)."""
    return sorted(data, key=lambda d: d["date"], reverse=is_reverse)
