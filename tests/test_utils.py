
import os
from datetime import datetime

import pandas as pd
import pytest
import requests
from pandas.testing import assert_frame_equal
from pytest_mock import MockFixture

from config import ROOT_DIR
from src.utils import form_data_frame, get_currency_rates, get_expenses, get_income, get_period

path_to_data = os.path.join(ROOT_DIR, "data")
path_to_test_df_tiny = os.path.join(path_to_data, "test_operations_2.xlsx")
path_to_test_df = os.path.join(path_to_data, "test_operations_1.xlsx")


def test_form_data_frame_correct() -> None:
    result_df = form_data_frame(path_to_test_df_tiny)
    date_1 = datetime.strptime('04.01.2018', "%d.%m.%Y").date()
    date_2 = datetime.strptime('01.01.2018', "%d.%m.%Y").date()
    expected_df = pd.DataFrame({'date': [date_1, date_2], 'amount': [-316, -3000], 'category': ['Красота', 'Переводы']})
    assert_frame_equal(result_df, expected_df)



def test_form_data_frame_no_file():
    with pytest.raises(FileNotFoundError):
        assert form_data_frame('no_file_path')

@pytest.mark.parametrize('date, period', [('31.12.2021', 'Y'), ('31.12.2021', 'W'), ('31.12.2021', 'D'), ('31.12.2021', 'M'), ('31.12.2021', 'ALL')])
def test_get_period_correct(date, period):
    result_df = get_period(date, period).head(1)
    date = datetime.strptime('31.12.2021', "%d.%m.%Y").date()
    expected_df = pd.DataFrame({'date': [date], 'amount': [-160.89], 'category': ['Супермаркеты']})
    assert_frame_equal(result_df, expected_df)

def test_get_period_incorrect():
    result_df = get_period('31.12.2035').head(1)
    assert result_df.empty

def test_get_expenses_correct():
    df = form_data_frame(path_to_test_df_tiny)
    assert get_expenses(df) == {'main': [{'Другое': 0, 'Красота': -316}], 'total_amount': -3316, 'transfers_and_cash': [{'Переводы': -3000}]}

def test_get_income_correct():
    df = form_data_frame(path_to_test_df)
    assert get_income(df) == {'main': [{'Пополнения': 179046}], 'total_amount': 179046}

def test_get_currency_rates_correct(mocker: MockFixture, mock_currency_response) -> None:
    mock_response = mocker.patch("requests.get")
    mock_response.return_value.json.return_value = {
        "success": True,
        "query": {"from": "USD", "to": "RUB", "amount": 8221.37},
        "info": {"timestamp": 1747777395, "rate": 80.624798},
        "date": "2025-05-20",
        "result": 662846.295533,
    }
    assert get_currency_rates() == mock_currency_response
    mock_response.assert_called()


def test_get_currency_rates_error(mocker: MockFixture):
    mock_response = mocker.patch("src.utils.requests.get", side_effect=requests.exceptions.ConnectionError)
    assert get_currency_rates() == "Ошибка обращения к api"
    mock_response.assert_called_once()

def test_get_stock_rates(monkeypatch, mock_stock_response):
    def mock_get_stock_rates():
        return mock_stock_response
    monkeypatch.setattr('src.utils.get_stock_rates', mock_get_stock_rates)
    from src.utils import get_stock_rates
    assert get_stock_rates() == mock_stock_response
