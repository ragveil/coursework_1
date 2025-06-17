import json

from src.constants import PATH_TO_OPERATIONS_XLSX
from src.utils import form_data_frame, get_currency_rates, get_expenses, get_income, get_period, get_stock_rates


def get_events_json(date: str, period: str = "M") -> str:
    """
    Объединяет работу функций из модуля utils.py.
    :param date: Входящее значение - дата, строка.
    :param period: Входящее значение - период, строка.
    :return: Результат работы функции, json.
    """
    form_data_frame(PATH_TO_OPERATIONS_XLSX)
    df = get_period(date, period)
    expenses = get_expenses(df)
    income = get_income(df)
    currency_rates = get_currency_rates()
    stock_rates = get_stock_rates()
    result = {"expenses": expenses, "income": income, "currency_rates": currency_rates, "stock_rates": stock_rates}
    return json.dumps(result, ensure_ascii=False)
