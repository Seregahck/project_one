import pytest

from src.masks import get_mask_account, get_mask_card_number
from src.widget import mask_account_card, get_date
from src.processing import filter_by_state, sort_by_date

def test_get_mask_card_number_valid():
    """Минимальный тест для get_mask_card_number"""
    assert get_mask_card_number("1234567890123456") == "1234 56** **** 3456"
    assert get_mask_card_number("1111222233334444") == "1111 22** **** 4444"


def test_get_mask_card_number_invalid():
    """Минимальный тест для невалидных карт"""
    with pytest.raises(ValueError):
        get_mask_card_number("123")  # слишком короткий
    with pytest.raises(ValueError):
        get_mask_card_number("1234abcd90123456")  # не цифры


def test_get_mask_account_valid():
    """Минимальный тест для get_mask_account"""
    assert get_mask_account("40817810570012345678") == "**5678"
    assert get_mask_account("1234") == "**1234"  # минимальная длина


def test_get_mask_account_invalid():
    """Минимальный тест для невалидных счетов"""
    with pytest.raises(ValueError):
        get_mask_account("123")  # слишком короткий
    with pytest.raises(ValueError):
        get_mask_account("1234-abcd")  # не цифры


def test_mask_account_card_card():
    """Минимальный тест для карты в mask_account_card"""
    assert mask_account_card("Visa 1234567890123456") == "Visa 1234 56** **** 3456"


def test_mask_account_card_account():
    """Минимальный тест для счета в mask_account_card"""
    assert mask_account_card("Счет 12345678901234567890") == "Счет **7890"


def test_get_date_valid():
    """Минимальный тест валидной даты"""
    assert get_date("2023-12-31") == "31.12.2023"


def test_get_date_invalid():
    """Минимальный тест невалидной даты"""
    assert get_date("") == ""
    assert get_date("not-a-date") == ""


def test_filter_by_state_basic():
    """Минимальный тест для filter_by_state"""
    transactions = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "PENDING"},
    ]

    result = filter_by_state(transactions, "EXECUTED")
    assert result == [{"id": 1, "state": "EXECUTED"}]


def test_filter_by_state_default():
    """Тест со значением по умолчанию"""
    transactions = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "PENDING"},
    ]

    result = filter_by_state(transactions)  # по умолчанию EXECUTED
    assert result == [{"id": 1, "state": "EXECUTED"}]


def test_sort_by_date_descending():
    """Минимальный тест сортировки по убыванию"""
    transactions = [
        {"id": 1, "date": "2023-01-01"},
        {"id": 2, "date": "2023-12-31"},
    ]

    result = sort_by_date(transactions)  # по умолчанию reverse=True
    assert result[0]["id"] == 2  # самая поздняя дата
    assert result[1]["id"] == 1


def test_sort_by_date_ascending():
    """Минимальный тест сортировки по возрастанию"""
    transactions = [
        {"id": 1, "date": "2023-01-01"},
        {"id": 2, "date": "2023-12-31"},
    ]

    result = sort_by_date(transactions, reverse=False)
    assert result[0]["id"] == 1  # самая ранняя дата
    assert result[1]["id"] == 2