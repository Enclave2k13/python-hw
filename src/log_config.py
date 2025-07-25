import logging
import os


def setup_logger(name, log_file, level=logging.DEBUG, encoding="utf-8"):
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    file_handler = logging.FileHandler(filename=f"logs/{log_file}", mode="w", encoding=encoding)

    file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)

    logger.addHandler(file_handler)
    return logger
