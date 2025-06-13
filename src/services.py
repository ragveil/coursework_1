import json
import os
import re
from typing import Any

from config import ROOT_DIR
from src.logger import get_logger

path = os.path.join(ROOT_DIR, "data", "operations.json")
logger = get_logger(__name__)

def get_transactions(path_to_file: str) -> Any:
    logger.info(f"Формирование транзакций из файла {path_to_file}")
    with open(path_to_file, "r", encoding="utf-8") as file:
        operations_data = json.load(file)
    logger.info('Список транзакций успешно сформирован')
    return operations_data


def search_item(transactions: list[dict], item: str) -> list[dict]|str:
    result = []
    logger.info(f'Начало работы функции поиска по ключевому слову. Ключевое слово {item}')
    for transaction in transactions:
        if re.search(item.lower(), transaction["Категория"].lower()) or re.search(item.lower(), transaction["Описание"].lower()) is not None:
            result.append(transaction)
    if len(result) == 0:
        logger.info('Совпадений не найдено')
        return 'Совпадений не найдено'
    logger.info('Успешное завершение функции')
    return json.dumps(result, ensure_ascii=False)


list_of_transactions = get_transactions(path)

# print(search_item(list_of_transactions, 'инвест'))
