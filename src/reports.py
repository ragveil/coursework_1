
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

data_frame = get_dataframe()
