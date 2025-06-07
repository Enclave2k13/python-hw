from masks import get_mask_account
from masks import get_mask_card_number


def mask_account_card(pay_info: str) -> str:
    """Обрабатывает информацию о картах и счетах и возвращает строку с замаскированным номером"""
    account = "Счет"
    if account == pay_info.split()[0]:
        return get_mask_account(pay_info.split()[-1])
    else:
        return get_mask_card_number(pay_info.split()[-1])
