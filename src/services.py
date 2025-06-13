import json
import os
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


list_of_transactions = get_transactions(path)