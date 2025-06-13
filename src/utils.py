import os
import re
from datetime import datetime, timedelta
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

def get_period(date: str, period: str = "M") -> Any:
    end_date = datetime.strptime(date, "%d.%m.%Y").date()
    logger.info("Формирование периода для работы с DataFrame")
    match period.upper():
        case 'M':
            start_date_replace = re.sub(r"^\d\d", "01", date)
            start_date = datetime.strptime(start_date_replace, "%d.%m.%Y").date()
            logger.info(f"Сформирован период - Месяц(M): {start_date} : {end_date}")
        case "W":
            day_of_week = end_date.weekday()
            start_date = end_date - timedelta(days=day_of_week)
            logger.info(f"Сформирован период - Неделя(W): {start_date} : {end_date}")
        case 'Y':
            start_date_replace = re.sub(r"^\d\d.\d\d", "01.01", date)
            start_date = datetime.strptime(start_date_replace, "%d.%m.%Y").date()
            logger.info(f"Сформирован период - Год(Y): {start_date} : {end_date}")
        case _:
            logger.info(f"Сформирован период - За всё время: {df_formed['date'].iloc[-1]} : {end_date}")
            return df_formed
    mask = (df_formed["date"] >= start_date) & (df_formed["date"] <= end_date)
    df = df_formed.loc[mask]
    return df



df_formed = form_data_frame()
