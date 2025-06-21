def filter_by_state(data: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Функция фильтрует словари по заданному ключу state"""
    filtered_data = []
    for user_dict in data:
        if user_dict.get("state") == state:
            filtered_data.append(user_dict)
    return filtered_data
