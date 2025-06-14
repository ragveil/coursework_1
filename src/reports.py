
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd

from src.utils import path


def get_dataframe() -> pd.DataFrame:
    columns: list|int = ['Дата операции','Дата платежа','Статус','Сумма платежа','Валюта платежа','Категория']
    df = pd.read_excel(str(path), usecols=columns, engine="openpyxl")
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
    df["Дата платежа"] = pd.to_datetime(df["Дата платежа"], dayfirst=True)
    df["Дата платежа"] = df["Дата операции"].dt.date
    df = df.drop(df[df["Статус"] == "FAILED"].index)
    df = df.drop(df[df["Валюта платежа"] != "RUB"].index)
    df = df.drop(columns=["Дата операции", 'Статус', 'Валюта платежа'])
    df = df[df["Сумма платежа"] < 0]
    return df


# Функция возвращает траты по заданной категории за последние три месяца (от переданной даты).
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None):
    if date:
        end_date = datetime.strptime(date, "%d.%m.%Y").date()
    else:
        end_date = datetime.today().date()
    period = timedelta(days=90)
    start_date = end_date - period
    mask = (transactions["Дата платежа"] >= start_date) & (transactions["Дата платежа"] <= end_date)
    df = transactions.loc[mask]
    try:
        df = df[df['Категория'] == category]
    except KeyError:
        return 'Неверно введена категория'
    else:
        df['Дата платежа'] = pd.to_datetime(df['Дата платежа']).dt.strftime('%d.%m.%Y')
        return df.to_dict(orient='records')


# Функция возвращает средние траты в каждый из дней недели за последние три месяца (от переданной даты).
def spending_by_weekday(transactions: pd.DataFrame,
                        date: Optional[str] = None):
    if date:
        end_date = datetime.strptime(date, "%d.%m.%Y").date()
    else:
        end_date = datetime.today().date()
    period = timedelta(days=90)
    start_date = end_date - period
    mask = (transactions["Дата платежа"] >= start_date) & (transactions["Дата платежа"] <= end_date)
    df = transactions.loc[mask]
    df.loc[:, 'Дата платежа'] = df.loc[:, 'Дата платежа'].apply(lambda x: x.weekday())
    grp = df.groupby('Дата платежа').agg({'Сумма платежа': 'mean'})
    result = {f'Средние траты по дням недели за период с {start_date.strftime('%d.%m.%Y')} по {end_date.strftime('%d.%m.%Y')}': {'Понедельник': int(grp.at[0, 'Сумма платежа']), 'Вторник': int(grp.at[1, 'Сумма платежа']), 'Среда': int(grp.at[2, 'Сумма платежа']), 'Четверг': int(grp.at[3, 'Сумма платежа']), 'Пятница': int(grp.at[4, 'Сумма платежа']), 'Суббота': int(grp.at[5, 'Сумма платежа']), 'Воскресенье': int(grp.at[6, 'Сумма платежа'])}}
    return result


data_frame = get_dataframe()
print(spending_by_category(data_frame, 'Супермаркеты', '08.05.2019'))
print(spending_by_weekday(data_frame, '01.03.2020'))
