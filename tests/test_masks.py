import pytest

from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state, sort_by_date
from src.widget import get_date, mask_account_card


def test_get_mask_card_number_valid(valid_card_numbers):
    """Тест с фикстурой valid_card_numbers"""
    assert get_mask_card_number(valid_card_numbers[0]) == "1234 56** **** 3456"
    assert get_mask_card_number(valid_card_numbers[1]) == "1111 22** **** 4444"


def test_get_mask_card_number_invalid(invalid_card_numbers):
    """Тест с фикстурой invalid_card_numbers"""
    for card_number, expected_error in invalid_card_numbers:
        with pytest.raises(ValueError, match=expected_error):
            get_mask_card_number(card_number)


def test_get_mask_card_number_with_spaces(card_numbers_with_spaces):
    """Тест номеров карт с пробелами"""
    for card_number in card_numbers_with_spaces:
        # Все варианты с пробелами должны давать одинаковый результат
        result = get_mask_card_number(card_number)
        assert result == "1234 56** **** 3456"


# 2. Тесты get_mask_account с фикстурами
def test_get_mask_account_valid(valid_account_numbers):
    """Тест с фикстурой valid_account_numbers"""
    assert get_mask_account(valid_account_numbers[0]) == "**5678"
    assert get_mask_account(valid_account_numbers[1]) == "**1234"


def test_get_mask_account_invalid(invalid_account_numbers):
    """Тест с фикстурой invalid_account_numbers"""
    for account_number, expected_error in invalid_account_numbers:
        with pytest.raises(ValueError, match=expected_error):
            get_mask_account(account_number)


def test_get_mask_account_with_spaces(account_numbers_with_spaces):
    """Тест номеров счетов с пробелами"""
    assert get_mask_account(account_numbers_with_spaces[0]) == "**5678"
    assert get_mask_account(account_numbers_with_spaces[1]) == "**1234"


# 3. Тесты mask_account_card с фикстурами
def test_mask_account_card_card(card_strings):
    """Тест с фикстурой card_strings"""
    assert mask_account_card(card_strings[0]) == "Visa 1234 56** **** 3456"
    assert mask_account_card(card_strings[1]) == "MasterCard 1111 22** **** 4444"


def test_mask_account_card_account(account_strings):
    """Тест с фикстурой account_strings"""
    assert mask_account_card(account_strings[0]) == "Счет **5678"
    assert mask_account_card(account_strings[1]) == "СЧЕТ **7890"


def test_mask_account_card_edge_cases(edge_strings):
    """Тест крайних случаев"""
    # Проверяем что функция не падает
    for string in edge_strings:
        result = mask_account_card(string)
        assert isinstance(result, str)


# 4. Тесты get_date с фикстурами
def test_get_date_valid(valid_dates):
    """Тест с фикстурой valid_dates"""
    assert get_date(valid_dates[0]) == "31.12.2023"
    assert get_date(valid_dates[1]) == "29.02.2024"
    assert get_date(valid_dates[2]) == "01.01.2023"


def test_get_date_invalid(invalid_dates):
    """Тест с фикстурой invalid_dates"""
    for date_str in invalid_dates:
        result = get_date(date_str)
        assert result == ""


# 5. Тесты filter_by_state с фикстурами
def test_filter_by_state_basic(sample_transactions):
    """Тест с фикстурой sample_transactions"""
    result = filter_by_state(sample_transactions, "EXECUTED")
    assert len(result) == 2
    assert all(t["state"] == "EXECUTED" for t in result)


def test_filter_by_state_default(sample_transactions):
    """Тест значения по умолчанию"""
    result = filter_by_state(sample_transactions)
    assert len(result) == 2
    assert all(t["state"] == "EXECUTED" for t in result)


def test_filter_by_state_all_executed(executed_transactions):
    """Тест когда все транзакции EXECUTED"""
    result = filter_by_state(executed_transactions, "EXECUTED")
    assert result == executed_transactions


def test_filter_by_state_pending(pending_transactions):
    """Тест фильтрации PENDING"""
    result = filter_by_state(pending_transactions, "PENDING")
    assert len(result) == 2
    assert all(t["state"] == "PENDING" for t in result)


def test_filter_by_state_empty(empty_transactions):
    """Тест с пустым списком"""
    result = filter_by_state(empty_transactions, "EXECUTED")
    assert result == []


def test_filter_by_state_single(single_transaction):
    """Тест с одной транзакцией"""
    result = filter_by_state(single_transaction, "EXECUTED")
    assert result == single_transaction


# 6. Тесты sort_by_date с фикстурами
def test_sort_by_date_descending(dated_transactions):
    """Тест сортировки по убыванию"""
    result = sort_by_date(dated_transactions)
    assert result[0]["id"] == 2  # самая поздняя дата
    assert result[1]["id"] == 3
    assert result[2]["id"] == 1  # самая ранняя дата


def test_sort_by_date_ascending(dated_transactions):
    """Тест сортировки по возрастанию"""
    result = sort_by_date(dated_transactions, reverse=False)
    assert result[0]["id"] == 1  # самая ранняя дата
    assert result[1]["id"] == 3
    assert result[2]["id"] == 2  # самая поздняя дата


def test_sort_by_date_chronological(chronological_transactions):
    """Тест с хронологическим порядком"""
    result = sort_by_date(chronological_transactions, reverse=False)
    assert [t["id"] for t in result] == [1, 2, 3, 4]


def test_sort_by_date_same_date(same_date_transactions):
    """Тест с одинаковыми датами"""
    result = sort_by_date(same_date_transactions)
    # При одинаковых датах порядок должен сохраниться
    assert [t["id"] for t in result] == [1, 2, 3]


def test_sort_by_date_empty(empty_transactions):
    """Тест сортировки пустого списка"""
    result = sort_by_date(empty_transactions)
    assert result == []


def test_sort_by_date_single(single_transaction):
    """Тест сортировки одной транзакции"""
    # Добавляем дату в транзакцию
    transaction_with_date = [{"id": 1, "date": "2023-01-01"}]
    result = sort_by_date(transaction_with_date)
    assert result == transaction_with_date


# 7. Параметризованные тесты
@pytest.mark.parametrize("state, expected_count", [
    ("EXECUTED", 2),
    ("PENDING", 1),
    ("CANCELED", 1),
    ("FAILED", 0),
])
def test_filter_by_state_parametrized(sample_transactions, state, expected_count):
    """Параметризованный тест фильтрации"""
    result = filter_by_state(sample_transactions, state)
    assert len(result) == expected_count
    if expected_count > 0:
        assert all(t["state"] == state for t in result)


@pytest.mark.parametrize("reverse, expected_order", [
    (True, [2, 3, 1]),  # по убыванию
    (False, [1, 3, 2]),  # по возрастанию
])
def test_sort_by_date_parametrized(dated_transactions, reverse, expected_order):
    """Параметризованный тест сортировки"""
    result = sort_by_date(dated_transactions, reverse=reverse)
    assert [t["id"] for t in result] == expected_order
