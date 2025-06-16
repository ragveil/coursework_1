import json
import os
from datetime import datetime
from typing import Any

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal
import freezegun
from config import ROOT_DIR
from src.reports import get_dataframe, save_to_file, spending_by_category, spending_by_weekday, spending_by_workday

path_to_logs = os.path.join(ROOT_DIR, "logs/")
path_to_data = os.path.join(ROOT_DIR, "data/")
path_to_test_df_tiny = os.path.join(path_to_data, "test_operations_2.xlsx")
path_to_test_df = os.path.join(path_to_data, "test_operations_1.xlsx")
path_to_filtered_df = os.path.join(path_to_data, "test_filtered_data.xlsx")

def test_get_data_frame_correct() -> None:
    result_df = get_dataframe(path_to_test_df_tiny)
    date = datetime.strptime('01.01.2018', "%d.%m.%Y").date()
    expected_df = pd.DataFrame({'Дата платежа': [date, date], 'Сумма платежа': [-316, -3000], 'Категория': ['Красота', 'Переводы']})
    assert_frame_equal(result_df, expected_df)

def test_form_data_frame_no_file():
    with pytest.raises(FileNotFoundError):
        assert get_dataframe('no_file_path')

def test_spending_by_category_correct(spending_by_category_correct) -> None:
    df = get_dataframe(path_to_test_df)
    assert spending_by_category(df, 'Супермаркеты', '31.12.2021') == spending_by_category_correct

@freezegun.freeze_time("2021-12-31")
def test_spending_by_category_today(spending_by_category_correct) -> None:
    df = get_dataframe(path_to_test_df)
    assert spending_by_category(df, 'Супермаркеты') == spending_by_category_correct

@pytest.mark.parametrize('category, date, expected', [('ЖКХ', '31.12.2021', []), ('Супермаркет', '31.12.2222', [])])
def test_spending_by_category_incorrect(category, date, expected) -> None:
    df = get_dataframe(path_to_test_df)
    assert spending_by_category(df, category, date) == expected

def test_spending_by_weekday_correct(spending_by_weekday_correct) -> None:
    df = get_dataframe(path_to_filtered_df)
    assert spending_by_weekday(df, '31.12.2021') == spending_by_weekday_correct

@freezegun.freeze_time("2021-12-31")
def test_spending_by_weekday_today(spending_by_weekday_correct) -> None:
    df = get_dataframe(path_to_filtered_df)
    assert spending_by_weekday(df) == spending_by_weekday_correct

def test_spending_by_workday_correct(spending_by_workday_correct) -> None:
    df = get_dataframe(path_to_filtered_df)
    assert spending_by_workday(df, '31.12.2021') == spending_by_workday_correct

@freezegun.freeze_time("2021-12-31")
def test_spending_by_workday_today(spending_by_workday_correct) -> None:
    df = get_dataframe(path_to_filtered_df)
    assert spending_by_workday(df) == spending_by_workday_correct

def test_summ_num_filename(capsys: Any) -> None:
    @save_to_file('some_file.json')
    def summ_num(a: int, b: int) -> int:
        return a + b
    summ_num(1, 2)
    with open(path_to_logs + "some_file.json", "r", encoding="UTF-8", newline="\n") as f:
        log_file = json.load(f)
        assert 3 == log_file

def test_summ_num_default(capsys: Any) -> None:
    @save_to_file()
    def summ_num(a: int, b: int) -> int:
        return a + b
    summ_num(4, 3)
    with open(path_to_logs + "report.json", "r", encoding="UTF-8", newline="\n") as f:
        log_file = json.load(f)
        assert 7 == log_file