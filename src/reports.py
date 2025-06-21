import json
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Callable, Literal, Optional

import pandas as pd

from src.constants import PATH_TO_LOGS, PATH_TO_OPERATIONS_XLSX
from src.logger import get_logger

xlsx_path = PATH_TO_OPERATIONS_XLSX
files_path = PATH_TO_LOGS
logger = get_logger(__name__)


def save_to_file(filename: Literal[False] | str = False) -> Callable[[Any], Any]:
    """
    Декоратор для функций-отчетов.
    :param filename: Входящее значение - имя файла, строка.
    :return: Результат работы функции.
    """

    def decorator(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = func(*args, **kwargs)
                if filename is False:
                    with open(files_path + "report.json", "w", encoding="utf-8") as file:
                        json.dump(result, file, ensure_ascii=False, indent=4)
                else:
                    with open(files_path + str(filename), "w", encoding="utf-8") as file:
                        json.dump(result, file, ensure_ascii=False, indent=4)
                return result
            except Exception as e:
                result = f"Во время работы функции {func.__name__} возникла ошибка: {e}"
                if filename is False:
                    with open(files_path + "report.json", "w", encoding="utf-8") as file:
                        file.write(result)
                else:
                    with open(files_path + str(filename), "w", encoding="utf-8") as file:
                        file.write(result)

        return wrapper

    return decorator


def get_dataframe(path: str) -> pd.DataFrame:
    """
    Формирует dataframe из excel-файла для дальнейшей работы.
    :param path: Входящее значение - путь, строка.
    :return: Результат работы функции, dataframe.
    """
    columns = ["Дата операции", "Дата платежа", "Статус", "Сумма платежа", "Валюта платежа", "Категория"]
    df = pd.read_excel(str(path), usecols=columns, engine="openpyxl")
    logger.info("Загрузка данных из XLSX-файла")
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
    df["Дата платежа"] = pd.to_datetime(df["Дата платежа"], dayfirst=True)
    df["Дата платежа"] = df["Дата операции"].dt.date
    df = df.drop(df[df["Статус"] == "FAILED"].index)
    df = df.drop(df[df["Валюта платежа"] != "RUB"].index)
    df = df.drop(columns=["Дата операции", "Статус", "Валюта платежа"])
    df = df[df["Сумма платежа"] < 0]
    logger.info("Дата фрейм успешно сформирован")
    return df


# Функция возвращает траты по заданной категории за последние три месяца (от переданной даты).
@save_to_file("spending.json")
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> list | str:
    """
    Подсчет трат по категории за период три месяца.
    :param transactions: Входящее значение - dataframe.
    :param category: Входящее значение - категория, строка.
    :param date: Входящее значение - дата, строка.
    :return: Результат работы функции, json-ответ.
    """
    logger.info("Старт функции по формированию трат по заданной категории")
    if date:
        end_date = datetime.strptime(date, "%d.%m.%Y").date()
        logger.info(f"Заданная дата - {date}")
    else:
        end_date = datetime.today().date()
        logger.info("Дата не была задана. Будет использована текущая дата.")
    period = timedelta(days=90)
    start_date = end_date - period
    mask = (transactions["Дата платежа"] >= start_date) & (transactions["Дата платежа"] <= end_date)
    df = transactions.loc[mask]
    df = df[df["Категория"] == category]
    df["Дата платежа"] = pd.to_datetime(df["Дата платежа"]).dt.strftime("%d.%m.%Y")
    logger.info("Список трат по заданной категории успешно сформирован")
    return df.to_dict(orient="records")


# Функция возвращает средние траты в каждый из дней недели за последние три месяца (от переданной даты).
@save_to_file()
def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> dict:
    """
    Подсчет усредненных трат по дням недели за период три месяца.
    :param transactions: Входящее значение - dataframe.
    :param date: Входящее значение - дата, строка.
    :return: Результат работы функции, json-ответ.
    """
    logger.info("Старт функции по формированию трат в каждой день недели.")
    if date:
        end_date = datetime.strptime(date, "%d.%m.%Y").date()
        logger.info(f"Начальная дата - {date}")
    else:
        end_date = datetime.today().date()
        logger.info("Начальная дата не была задана. Будет использована текущая дата.")
    period = timedelta(days=90)
    start_date = end_date - period
    mask = (transactions["Дата платежа"] >= start_date) & (transactions["Дата платежа"] <= end_date)
    df = transactions.loc[mask]
    df.loc[:, "Дата платежа"] = df.loc[:, "Дата платежа"].apply(lambda x: x.weekday())
    grp = df.groupby("Дата платежа").agg({"Сумма платежа": "mean"})
    result = {
        "Средние траты по дням недели за период "
        f"с {start_date.strftime('%d.%m.%Y')} по {end_date.strftime('%d.%m.%Y')}": {
            "Понедельник": int(grp.at[0, "Сумма платежа"]),
            "Вторник": int(grp.at[1, "Сумма платежа"]),
            "Среда": int(grp.at[2, "Сумма платежа"]),
            "Четверг": int(grp.at[3, "Сумма платежа"]),
            "Пятница": int(grp.at[4, "Сумма платежа"]),
            "Суббота": int(grp.at[5, "Сумма платежа"]),
            "Воскресенье": int(grp.at[6, "Сумма платежа"]),
        }
    }
    logger.info("Список трат по дням недели успешно сформирован.")
    return result


# Функция выводит средние траты в рабочий и в выходной день за последние три месяца (от переданной даты).
@save_to_file("workdays.json")
def spending_by_workday(transactions: pd.DataFrame, date: Optional[str] = None) -> dict:
    """
    Подсчет усредненных трат по рабочим/выходным дням за период три месяца.
    :param transactions: Входящее значение - dataframe.
    :param date: Входящее значение - дата, строка.
    :return: Результат работы функции, json-ответ.
    """
    logger.info("Начало работы функции по формированию средних значений трат в рабочие и выходные дни.")
    if date:
        end_date = datetime.strptime(date, "%d.%m.%Y").date()
        logger.info(f"Начальная дата - {date}")
    else:
        end_date = datetime.today().date()
        logger.info("Начальная дата не была задана. Будет использована текущая дата.")
    period = timedelta(days=90)
    start_date = end_date - period
    mask = (transactions["Дата платежа"] >= start_date) & (transactions["Дата платежа"] <= end_date)
    df = transactions.loc[mask]
    df.loc[:, "Дата платежа"] = df.loc[:, "Дата платежа"].apply(lambda x: x.weekday())
    workdays_mask = df["Дата платежа"] <= 4
    workdays: Any = df.loc[workdays_mask]
    weekends_mask = df["Дата платежа"] >= 5
    weekends: Any = df.loc[weekends_mask]
    workdays = int(workdays["Сумма платежа"].mean())
    weekends = int(weekends["Сумма платежа"].mean())
    result = {
        f"Средние траты за период с {start_date.strftime('%d.%m.%Y')} по {end_date.strftime('%d.%m.%Y')}": {
            "Траты в рабочие дни": workdays,
            "Траты в выходные дни": weekends,
        }
    }
    logger.info("Список средних значений трат по выходным и будним дням успешно сформирован.")
    return result


data_frame = get_dataframe(xlsx_path)
