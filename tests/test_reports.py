from datetime import datetime

import freezegun
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from src.constants import DF_FOR_TESTS, FILTERED_DF_FOR_TESTS, PATH_TO_LOGS, TINY_DF_FOR_TESTS
from src.reports import get_dataframe, save_to_file, spending_by_category, spending_by_weekday, spending_by_workday

path_to_logs = PATH_TO_LOGS
path_to_test_df_tiny = TINY_DF_FOR_TESTS
path_to_test_df = DF_FOR_TESTS
path_to_filtered_df = FILTERED_DF_FOR_TESTS


def test_get_data_frame_correct() -> None:
    result_df = get_dataframe(path_to_test_df_tiny)
    date = datetime.strptime("01.01.2018", "%d.%m.%Y").date()
    expected_df = pd.DataFrame(
        {"Дата платежа": [date, date], "Сумма платежа": [-316, -3000], "Категория": ["Красота", "Переводы"]}
    )
    assert_frame_equal(result_df, expected_df)


def test_form_data_frame_no_file() -> None:
    with pytest.raises(FileNotFoundError):
        assert get_dataframe("no_file_path")


def test_spending_by_category_correct(spending_by_category_correct: list[dict]) -> None:
    df = get_dataframe(path_to_test_df)
    assert spending_by_category(df, "Супермаркеты", "31.12.2021") == spending_by_category_correct


@freezegun.freeze_time("2021-12-31")
def test_spending_by_category_today(spending_by_category_correct: list[dict]) -> None:
    df = get_dataframe(path_to_test_df)
    assert spending_by_category(df, "Супермаркеты") == spending_by_category_correct


@pytest.mark.parametrize("category, date, expected", [("ЖКХ", "31.12.2021", []), ("Супермаркет", "31.12.2222", [])])
def test_spending_by_category_incorrect(category: str, date: str, expected: list) -> None:
    df = get_dataframe(path_to_test_df)
    assert spending_by_category(df, category, date) == expected


def test_spending_by_weekday_correct(spending_by_weekday_correct: dict) -> None:
    df = get_dataframe(path_to_filtered_df)
    assert spending_by_weekday(df, "31.12.2021") == spending_by_weekday_correct


@freezegun.freeze_time("2021-12-31")
def test_spending_by_weekday_today(spending_by_weekday_correct: dict) -> None:
    df = get_dataframe(path_to_filtered_df)
    assert spending_by_weekday(df) == spending_by_weekday_correct


def test_spending_by_workday_correct(spending_by_workday_correct: dict) -> None:
    df = get_dataframe(path_to_filtered_df)
    assert spending_by_workday(df, "31.12.2021") == spending_by_workday_correct


@freezegun.freeze_time("2021-12-31")
def test_spending_by_workday_today(spending_by_workday_correct: dict) -> None:
    df = get_dataframe(path_to_filtered_df)
    assert spending_by_workday(df) == spending_by_workday_correct


def test_zero_division_filename(zero_division_decor: str) -> None:
    @save_to_file("some_file.json")
    def zero_division(a: int, b: int) -> float:
        return a / b

    zero_division(4, 2)
    zero_division(4, 0)
    with open(path_to_logs + "some_file.json", "r", encoding="UTF-8", newline="\n") as f:
        log_file = f.read()
        assert zero_division_decor == log_file


def test_zero_division_default(zero_division_decor: str) -> None:
    @save_to_file()
    def zero_division(a: int, b: int) -> float:
        return a / b

    zero_division(4, 2)
    zero_division(4, 0)
    with open(path_to_logs + "report.json", "r", encoding="UTF-8", newline="\n") as f:
        log_file = f.read()
        assert zero_division_decor == log_file
