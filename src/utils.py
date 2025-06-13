import json
import os
import re
from datetime import datetime, timedelta
from itertools import islice
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv

from config import ROOT_DIR
from src.logger import get_logger

logger = get_logger(__name__)

load_dotenv()
api_token = os.getenv("API_TOKEN")
api_url = os.getenv("API_URL")

settings = os.path.join(ROOT_DIR, "user_settings.json")
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


def get_expenses(data_frame: pd.DataFrame) -> dict:
    logger.info("Начало работы функции по подсчету расходов за выбранный период")
    expenses_df = data_frame[data_frame["amount"] < 0]
    expenses_general = {}
    expenses_cash = {}
    list_of_categories = ["Переводы", "Наличные", "Другое", "Различные товары"]
    amount_df = expenses_df.groupby("category")["amount"].sum().sort_values(ascending=True)
    logger.info("Сводная таблица расходов успешно сформирована")
    for item, value in zip(amount_df.index, amount_df.values):
        if item not in list_of_categories:
            expenses_general[item] = int(value)
        elif item in ("Переводы", "Наличные"):
            expenses_cash[item] = int(value)
        else:
            pass
    expenses_new = dict(islice(expenses_general.items(), 5))
    other_expenses = 0
    list_1 = [*expenses_new.keys(), *expenses_cash.keys()]
    for item, value in zip(amount_df.index, amount_df.values):
        if str(item) not in list_1:
            other_expenses += int(value)
    expenses_new["Другое"] = other_expenses
    expenses = {
        "total_amount": int(amount_df.iloc[:].sum()),
        "main": [expenses_new],
        "transfers_and_cash": [expenses_cash],
    }
    logger.info("Успешное выполнение функции и формирование корректного JSON-ответа")
    return expenses


def get_income(data_frame: pd.DataFrame) -> dict:
    logger.info("Начало работы функции по подсчету доходов за выбранный период")
    income_df = data_frame[data_frame["amount"] > 0]
    income_general = {}
    amount_df = income_df.groupby("category")["amount"].sum().sort_values(ascending=False)
    logger.info("Сводная таблица доходов успешно сформирована")
    for item, value in zip(amount_df.index, amount_df.values):
        income_general[item] = int(value)
    income = {"total_amount": int(amount_df.iloc[:].sum()), "main": [income_general]}
    logger.info("Успешное выполнение функции и формирование корректного JSON-ответа")
    return income


def get_currency_rates() -> list|str:
    logger.info("Начало работы функции по получению курсов валют")
    with open(settings, "r", encoding="utf-8") as file:
        currency_list = json.load(file)["user_currencies"]
        currency_rates = []
    for currency in currency_list:
        params = {"amount": 1, "to": "RUB", "from": currency}
        headers = {"apikey": api_token}
        try:
            response: Any = requests.get(api_url, headers=headers, params=params, timeout=50)
            status = response.raise_for_status()
            logger.info(f"Попытка соединения с сервером, {status}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка обращения к api {e}")
            return "Ошибка обращения к api"
        else:
            temp = {"currency": currency, "rate": round(response.json().get("info").get("rate"), 2)}
            currency_rates.append(temp)
            logger.info("Успешное получение данных о курсе валют и формирование корректного JSON-ответа")
    return currency_rates


df_formed = form_data_frame()
df_got_date = get_period("12.03.2020", "asd")
get_expenses(df_got_date)
get_income(df_got_date)