def get_mask_card_number(card_number: str) -> str:
    """Функция проверяет размер номера банковской карты на корректность и затем маскирует ее в формате
    XXXX XX** **** XXXX"""
    if (len(card_number)) != 16 or not card_number.isdigit():
        raise ValueError("Номер карты должен состоять из 16 цифр")

    return f"{card_number[:4]} {card_number[5:7]}** **** {card_number[-4:]}"


def get_mask_account(account_number: str) -> str:
    """Функция маскирует номер банковского счета в формате **XXXX"""
    if not account_number.isdigit():
        raise ValueError("Номер счета должен состоять из цифр")

    return f"**{account_number[-4:]}"
