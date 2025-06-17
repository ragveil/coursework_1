import logging

from src.constants import LOGS_DEFAULT

logs_path = LOGS_DEFAULT
logging_format = "%(asctime)s - %(name)s - %(levelname)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"


def get_file_handler() -> logging.FileHandler:
    file_handler = logging.FileHandler(logs_path, encoding="utf-8", mode="w")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(logging_format))
    return file_handler


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_file_handler())
    return logger
