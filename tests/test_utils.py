from datetime import datetime
from typing import Any

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal
from pytest_mock import MockFixture
from requests import ConnectionError

from src.constants import DF_FOR_TESTS, PATH_TO_DATA, TINY_DF_FOR_TESTS
from src.utils import form_data_frame, get_currency_rates, get_expenses, get_income, get_period

path_to_data = PATH_TO_DATA
path_to_test_df_tiny = TINY_DF_FOR_TESTS
path_to_test_df = DF_FOR_TESTS


def test_form_data_frame_correct() -> None:
    result_df = form_data_frame(path_to_test_df_tiny)
    date_1 = datetime.strptime("01.01.2018", "%d.%m.%Y").date()
    date_2 = datetime.strptime("01.01.2018", "%d.%m.%Y").date()
    expected_df = pd.DataFrame(
        {"date": [date_1, date_2], "amount": [-316, -3000], "category": ["Красота", "Переводы"]}
    )
    assert_frame_equal(result_df, expected_df)


def test_form_data_frame_no_file() -> None:
    with pytest.raises(FileNotFoundError):
        assert form_data_frame("no_file_path")


@pytest.mark.parametrize(
    "date, period",
    [("31.12.2021", "Y"), ("31.12.2021", "W"), ("31.12.2021", "D"), ("31.12.2021", "M"), ("31.12.2021", "ALL")],
)
def test_get_period_correct(date: str, period: str) -> None:
    result_df = get_period(date, period).head(1)
    date_ = datetime.strptime("31.12.2021", "%d.%m.%Y").date()
    expected_df = pd.DataFrame({"date": [date_], "amount": [-160.89], "category": ["Супермаркеты"]})
    assert_frame_equal(result_df, expected_df)


def test_get_period_incorrect() -> None:
    result_df = get_period("31.12.2035").head(1)
    assert result_df.empty


def test_get_expenses_correct() -> None:
    df = form_data_frame(path_to_test_df_tiny)
    assert get_expenses(df) == {
        "main": [{"Другое": 0, "Красота": -316}],
        "total_amount": -3316,
        "transfers_and_cash": [{"Переводы": -3000}],
    }


def test_get_income_correct() -> None:
    df = form_data_frame(path_to_test_df)
    assert get_income(df) == {"main": [{"Пополнения": 179046}], "total_amount": 179046}


def test_get_currency_rates_correct(mocker: MockFixture, mock_currency_response: list[dict]) -> None:
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


def test_get_currency_rates_error(mocker: MockFixture) -> None:
    mock_response = mocker.patch("src.utils.requests.get", side_effect=ConnectionError)
    assert get_currency_rates() == "Ошибка обращения к api"
    mock_response.assert_called_once()


def test_get_stock_rates(monkeypatch: Any, mock_stock_response: list[dict]) -> None:
    def mock_get_stock_rates() -> Any:
        return mock_stock_response

    monkeypatch.setattr("src.utils.get_stock_rates", mock_get_stock_rates)
    from src.utils import get_stock_rates

    assert get_stock_rates() == mock_stock_response
