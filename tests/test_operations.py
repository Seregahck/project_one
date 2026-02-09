import pytest
from datetime import datetime
from operations import (
    process_bank_search,
    process_bank_operations,
    filter_by_status,
    sort_transactions,
    filter_rub_transactions,
    mask_account_number,
    format_transaction
)

# Тестовые данные
TEST_TRANSACTIONS = [
    {
        "id": 1,
        "date": "2024-01-15T14:30:00Z",
        "state": "EXECUTED",
        "description": "Оплата в ресторане",
        "from": "MasterCard 1234 5678 9012 3456",
        "to": "Счет 12345678901234567890",
        "operationAmount": {
            "amount": "100.50",
            "currency": {
                "name": "руб.",
                "code": "RUB"
            }
        }
    },
    {
        "id": 2,
        "date": "2024-01-14T10:15:00Z",
        "state": "EXECUTED",
        "description": "Перевод организации",
        "from": "Visa 1111 2222 3333 4444",
        "to": "Счет 98765432109876543210",
        "operationAmount": {
            "amount": "500.00",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        }
    },
    {
        "id": 3,
        "date": "2024-01-13T09:00:00Z",
        "state": "CANCELED",
        "description": "Оплата в супермаркете",
        "from": "Счет 11112222333344445555",
        "to": "Счет 55556666777788889999",
        "operationAmount": {
            "amount": "75.30",
            "currency": {
                "name": "руб.",
                "code": "RUB"
            }
        }
    },
    {
        "id": 4,
        "date": "2024-01-12T16:45:00Z",
        "state": "EXECUTED",
        "description": "Перевод с карты на карту",
        "from": "Maestro 1234567812345678",
        "to": "Visa 8765432187654321",
        "operationAmount": {
            "amount": "200.00",
            "currency": {
                "name": "EUR",
                "code": "EUR"
            }
        }
    },
    {
        "id": 5,
        "date": "2024-01-11T12:00:00Z",
        "state": "PENDING",
        "description": "Оплата в кафе",
        "from": "MasterCard 9999 8888 7777 6666",
        "to": "Счет 1234123412341234",
        "operationAmount": {
            "amount": "50.00",
            "currency": {
                "name": "руб.",
                "code": "RUB"
            }
        }
    }
]


# Тесты для process_bank_search
def test_process_bank_search_exact_match():
    """Тест поиска по точному совпадению."""
    result = process_bank_search(TEST_TRANSACTIONS, "ресторане")
    assert len(result) == 1
    assert result[0]["id"] == 1


def test_process_bank_search_partial_match():
    """Тест поиска по частичному совпадению."""
    result = process_bank_search(TEST_TRANSACTIONS, "Оплата")
    assert len(result) == 3
    ids = {t["id"] for t in result}
    assert ids == {1, 3, 5}


def test_process_bank_search_case_insensitive():
    """Тест регистронезависимого поиска."""
    result = process_bank_search(TEST_TRANSACTIONS, "ОПЛАТА")
    assert len(result) == 3


def test_process_bank_search_regex():
    """Тест поиска с использованием регулярных выражений."""
    # Поиск по началу строки
    result = process_bank_search(TEST_TRANSACTIONS, "^Перевод")
    assert len(result) == 2
    ids = {t["id"] for t in result}
    assert ids == {2, 4}


def test_process_bank_search_no_match():
    """Тест поиска, когда нет совпадений."""
    result = process_bank_search(TEST_TRANSACTIONS, "НесуществующееОписание")
    assert len(result) == 0


def test_process_bank_search_empty_input():
    """Тест поиска с пустыми входными данными."""
    result = process_bank_search([], "ресторане")
    assert len(result) == 0

    result = process_bank_search(TEST_TRANSACTIONS, "")
    assert len(result) == 0


# Тесты для process_bank_operations
def test_process_bank_operations_specific_categories():
    """Тест подсчета операций по конкретным категориям."""
    categories = ["Оплата", "Перевод"]
    result = process_bank_operations(TEST_TRANSACTIONS, categories)

    assert result["Оплата"] == 3  # 3 оплаты
    assert result["Перевод"] == 2  # 2 перевода


def test_process_bank_operations_partial_category():
    """Тест подсчета операций по частичному названию категории."""
    categories = ["организации", "кафе"]
    result = process_bank_operations(TEST_TRANSACTIONS, categories)

    assert result["организации"] == 1  # "Перевод организации"
    assert result["кафе"] == 1  # "Оплата в кафе"


def test_process_bank_operations_case_insensitive():
    """Тест регистронезависимого подсчета."""
    categories = ["ОПЛАТА", "перевод"]
    result = process_bank_operations(TEST_TRANSACTIONS, categories)

    assert result["ОПЛАТА"] == 3
    assert result["перевод"] == 2


def test_process_bank_operations_empty_transactions():
    """Тест подсчета операций с пустым списком транзакций."""
    result = process_bank_operations([], ["Оплата"])
    assert result == {}


def test_process_bank_operations_empty_categories():
    """Тест подсчета операций с пустым списком категорий."""
    result = process_bank_operations(TEST_TRANSACTIONS, [])
    assert result == {}


# Тесты для filter_by_status
def test_filter_by_status_executed():
    """Тест фильтрации по статусу EXECUTED."""
    result = filter_by_status(TEST_TRANSACTIONS, "EXECUTED")
    assert len(result) == 2
    ids = {t["id"] for t in result}
    assert ids == {1, 2}


def test_filter_by_status_case_insensitive():
    """Тест фильтрации по статусу в разном регистре."""
    result1 = filter_by_status(TEST_TRANSACTIONS, "executed")
    result2 = filter_by_status(TEST_TRANSACTIONS, "EXECUTED")
    assert len(result1) == len(result2) == 2


def test_filter_by_status_invalid():
    """Тест фильтрации по несуществующему статусу."""
    result = filter_by_status(TEST_TRANSACTIONS, "INVALID")
    assert len(result) == 0


# Тесты для sort_transactions
def test_sort_transactions_ascending():
    """Тест сортировки по возрастанию."""
    sorted_transactions = sort_transactions(TEST_TRANSACTIONS, reverse=False)
    dates = [datetime.fromisoformat(t["date"].replace('Z', '+00:00'))
             for t in sorted_transactions]
    assert dates == sorted(dates)


def test_sort_transactions_descending():
    """Тест сортировки по убыванию."""
    sorted_transactions = sort_transactions(TEST_TRANSACTIONS, reverse=True)
    dates = [datetime.fromisoformat(t["date"].replace('Z', '+00:00'))
             for t in sorted_transactions]
    assert dates == sorted(dates, reverse=True)


# Тесты для filter_rub_transactions
def test_filter_rub_transactions():
    """Тест фильтрации рублевых транзакций."""
    result = filter_rub_transactions(TEST_TRANSACTIONS)
    assert len(result) == 3
    ids = {t["id"] for t in result}
    assert ids == {1, 3, 5}


# Тесты для mask_account_number
def test_mask_account_number_card():
    """Тест маскирования номера карты."""
    result = mask_account_number("MasterCard 1234567890123456")
    assert result == "MasterCard 1234 56** **** 3456"


def test_mask_account_number_account():
    """Тест маскирования номера счета."""
    result = mask_account_number("Счет 12345678901234567890")
    assert result == "Счет **7890"


def test_mask_account_number_empty():
    """Тест маскирования пустой строки."""
    result = mask_account_number("")
    assert result == ""


def test_mask_account_number_invalid():
    """Тест маскирования некорректного номера."""
    result = mask_account_number("Invalid Number")
    assert result == "Invalid Number"


# Тесты для format_transaction
def test_format_transaction():
    """Тест форматирования транзакции."""
    transaction = TEST_TRANSACTIONS[0]
    formatted = format_transaction(transaction)

    assert "15.01.2024" in formatted
    assert "Оплата в ресторане" in formatted
    assert "MasterCard 1234 56** **** 3456" in formatted
    assert "Счет **7890" in formatted
    assert "Сумма: 100.50 руб." in formatted


# Интеграционные тесты
def test_full_pipeline():
    """Тест полного пайплайна обработки транзакций."""
    # Фильтрация по статусу
    executed = filter_by_status(TEST_TRANSACTIONS, "EXECUTED")
    assert len(executed) == 2

    # Сортировка
    sorted_transactions = sort_transactions(executed, reverse=True)
    assert sorted_transactions[0]["id"] == 1  # Более поздняя дата

    # Поиск
    searched = process_bank_search(sorted_transactions, "ресторане")
    assert len(searched) == 1
    assert searched[0]["id"] == 1

    # Подсчет категорий
    counts = process_bank_operations(searched, ["ресторане"])
    assert counts["ресторане"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])