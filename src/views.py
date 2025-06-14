import json

from src.utils import form_data_frame, get_currency_rates, get_expenses, get_income, get_period, get_stock_rates


def get_events_json(date: str, period: str ='M'):
    form_data_frame()
    df = get_period(date, period)
    expenses = get_expenses(df)
    income = get_income(df)
    currency_rates = get_currency_rates()
    stock_rates = get_stock_rates()
    result = {'expenses': expenses, 'income': income, 'currency_rates': currency_rates, 'stock_rates': stock_rates}
    return json.dumps(result, ensure_ascii=False)

print(get_events_json('01.03.2020', 'w'))
