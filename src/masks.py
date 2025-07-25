from log_config import setup_logger

logger = setup_logger("masks", "masks.log")


def get_mask_card_number(card_number: str) -> str:
    """Функция проверяет размер номера банковской карты на корректность и затем маскирует ее в формате
    XXXX XX** **** XXXX"""
    try:
        logger.debug(f"Начало маскирования карты: {card_number}")

        if card_number is None:
            error_msg = "Номер карты не может быть None"
            logger.error(error_msg)
            raise ValueError(error_msg)

        if (len(card_number)) != 16 or not card_number.isdigit():
            error_msg = "Номер карты должен состоять из 16 цифр"
            logger.error(error_msg)
            raise ValueError(error_msg)

        masked_number = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
        logger.info(f"Успешное маскирование карты. Результат: {masked_number}")

        return masked_number

    except Exception as e:
        logger.exception(f"Ошибка при маскировании карты: {str(e)}")
        raise


def get_mask_account(account_number: str) -> str:
    """Функция маскирует номер банковского счета в формате **XXXX"""
    try:
        logger.debug(f"Начало маскирования счета: {account_number}")

        if account_number is None:
            error_msg = "Номер счета не может быть None"
            logger.error(error_msg)
            raise ValueError(error_msg)

        if (len(account_number)) < 6 or not account_number.isdigit():
            error_msg = "Номер счета должен состоять из цифр"
            logger.error(error_msg)
            raise ValueError(error_msg)

        masked_account = f"**{account_number[-4:]}"
        logger.info(f"Успешное маскирование счета. Результат: {masked_account}")

        return masked_account

    except Exception as e:
        logger.exception(f"Ошибка при маскировании счета: {str(e)}")
        raise
