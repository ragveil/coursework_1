import json
import re
from typing import Any

from src.constants import PATH_TO_OPERATIONS_JSON
from src.logger import get_logger

path = PATH_TO_OPERATIONS_JSON
logger = get_logger(__name__)


def get_transactions(path_to_file: str) -> Any:
    """
    Создает список словарей для работы функций модуля.
    :param path_to_file: Входящее значение - путь к файлу, строка.
    :return: Результат работы функции, список.
    """
    logger.info(f"Формирование транзакций из файла {path_to_file}")
    with open(path_to_file, "r", encoding="utf-8") as file:
        operations_data = json.load(file)
    logger.info("Список транзакций успешно сформирован")
    return operations_data


def search_item(transactions: list[dict], item: str) -> str:
    """
    Простой поиск по ключевому слову.
    :param transactions: Входящее значение - список транзакций.
    :param item: Входящее значение - ключевое слово, строка.
    :return: Результат работы функции, json-объект.
    """
    result = []
    logger.info(f"Начало работы функции поиска по ключевому слову. Ключевое слово {item}")
    for transaction in transactions:
        if (
            re.search(item.lower(), transaction["Категория"].lower())
            or re.search(item.lower(), transaction["Описание"].lower()) is not None
        ):
            result.append(transaction)
    if len(result) == 0:
        logger.info("Совпадений не найдено")
        return "Совпадений не найдено"
    logger.info("Успешное завершение функции")
    return json.dumps(result, ensure_ascii=False)


def search_telephone_numbers(transactions: list[dict]) -> str:
    """
    Поиск по телефонным номерам.
    :param transactions: Входящее значение - список транзакций.
    :return: Результат работы функции, json-объект.
    """
    result = []
    logger.info("Начало работы функции поиска по номерам телефонов.")
    for transaction in transactions:
        if re.search(r"[+7]\s\d{3}\s\d{3}-\d{2}-\d{2}", transaction["Описание"]) is not None:
            result.append(transaction)
    if len(result) == 0:
        logger.info("Совпадений не найдено")
        return "Телефонных номеров не найдено"
    logger.info("Успешное завершение функции")
    return json.dumps(result, ensure_ascii=False)


def search_personal_transactions(transactions: list[dict]) -> str:
    """
    Поиск переводов физическим лицам.
    :param transactions: Входящее значение - список транзакций.
    :return: Результат работы функции, json-объект.
    """
    result = []
    logger.info("Начало работы функции поиска по именам.")
    for transaction in transactions:
        if transaction["Категория"] == "Переводы" and re.search(r"\w{3,}\s\w\.$", transaction["Описание"]) is not None:
            result.append(transaction)
    if len(result) == 0:
        logger.info("Совпадений не найдено")
        return "Переводов физическим лицам не найдено"
    logger.info("Успешное завершение функции")
    return json.dumps(result, ensure_ascii=False)


list_of_transactions = get_transactions(path)
