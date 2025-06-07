def get_mask_card_number(user_card_number: int) -> str:
    """Функция проверяет размер номера банковской карты на корректность и затем маскирует ее в формате
    XXXX XX** **** XXXX"""
    card_number = str(user_card_number)
    if (len(card_number)) != 16:
        raise ValueError("Номер карты должен состоять из 16 цифр")

    return f"{card_number[:4]} {card_number[5:7]}** **** {card_number[-4:]}"


def get_mask_account(user_account_number: int) -> str:
    """Функция маскирует номер банковского счета в формате **XXXX"""
    account_number = str(user_account_number)
    return f"**{account_number[-4:]}"
