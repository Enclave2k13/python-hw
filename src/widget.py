from dateutil.parser import parse

from masks import get_mask_account
from masks import get_mask_card_number


def mask_account_card(pay_info: str) -> str:
    """Обрабатывает информацию о картах и счетах и возвращает строку с замаскированным номером"""
    account = "Счет"
    if account == pay_info.split()[0]:
        return get_mask_account(pay_info.split()[-1])
    else:
        return get_mask_card_number(pay_info.split()[-1])


def get_date(date_string: str) -> str:
    """Смена даты с формата ISO на 'ДД.ММ.ГГГГ'"""
    date = parse(date_string)  # datetime format
    formatted_date = date.strftime("%d.%m.%Y")
    return formatted_date
