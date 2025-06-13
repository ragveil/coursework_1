
import os
from typing import Any

import pandas as pd

from config import ROOT_DIR
from src.logger import get_logger

logger = get_logger(__name__)


path = os.path.join(ROOT_DIR, "data", "operations.xlsx")


def form_data_frame() -> Any:
    df_columns: list | int = [
        "Дата платежа",
        "Статус",
        "Сумма платежа",
        "Валюта платежа",
        "Категория",
    ]
    df = pd.read_excel(str(path), usecols=df_columns, engine="openpyxl")
    logger.info("Успешная загрузка данных")
    df.columns = ["date", "status", "amount", "currency", "category"]
    df["date"] = pd.to_datetime(df["date"], dayfirst=True).dt.date
    df = df.drop (df[(df["status"] == "FAILED") | (df["currency"] != "RUB")].index)
    df = df.drop(columns=['status', 'currency'])
    logger.info("DataFrame сформирован")
    return df
