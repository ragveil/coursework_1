import json
from unittest.mock import mock_open, patch

import pytest

from src.services import get_transactions, search_item, search_personal_transactions, search_telephone_numbers


def test_get_transactions_correct(json_sample: list[dict[str, str | int]]) -> None:
    with patch("builtins.open", mock_open(read_data=json.dumps(json_sample))) as mock_file:
        assert get_transactions("builtins.open") == json_sample
        mock_file.assert_called_once_with("builtins.open", "r", encoding="utf-8")


def test_get_transactions_decode_error(wrong_json_list: list[dict[str, str | int]]) -> None:
    with patch("builtins.open", mock_open(read_data=str(wrong_json_list))) as mock_file:
        with pytest.raises(json.JSONDecodeError) as e:
            assert get_transactions("builtins.open") == e
            mock_file.assert_called_once_with("builtins.open", "r", encoding="utf-8")


def test_get_transactions_no_file() -> None:
    with pytest.raises(FileNotFoundError) as e:
        assert get_transactions("wrong_path") == e

def test_search_item_correct(transactions, simple_search_expected) -> None:
    assert search_item(transactions, 'супермаркет') == simple_search_expected

@pytest.mark.parametrize('keyword, expected', [('RUB', 'Совпадений не найдено'), ('слово', 'Совпадений не найдено')])
def test_search_item_incorrect(transactions, keyword, expected) -> None:
    assert search_item(transactions, keyword) == expected

def test_search_item_empty():
    assert search_item([], 'супермаркет') == 'Совпадений не найдено'

def test_search_telephone_numbers(transactions, telephone_numbers_expected) -> None:
    assert search_telephone_numbers(transactions) == telephone_numbers_expected

def test_search_telephone_numbers_empty() -> None:
    assert search_telephone_numbers([]) == 'Телефонных номеров не найдено'

def test_search_personal_transactions(transactions, personal_search_expected) -> None:
    assert search_personal_transactions(transactions) == personal_search_expected

def test_search_personal_transactions_empty() -> None:
    assert search_personal_transactions([]) == 'Переводов физическим лицам не найдено'
