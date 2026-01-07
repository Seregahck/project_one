import pytest

from src.generators import filter_by_currency, transaction_descriptions, card_number_generator

SAMPLE_TRANSACTIONS = [
    {"id": 1, "operationAmount": {"currency": {"code": "USD"}}, "description": "Payment 1"},
    {"id": 2, "operationAmount": {"currency": {"code": "EUR"}}, "description": "Payment 2"},
    {"id": 3, "operationAmount": {"currency": {"code": "USD"}}, "description": "Payment 3"},
    {"description": "No amount"}
]


def test_filter_by_currency_basic():
    """Минимальный тест filter_by_currency"""
    from generators import filter_by_currency
    result = list(filter_by_currency(SAMPLE_TRANSACTIONS, "USD"))
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 3


def test_filter_by_currency_empty():
    """Тест пустого результата"""
    from generators import filter_by_currency

    result = list(filter_by_currency(SAMPLE_TRANSACTIONS, "GBP"))
    assert len(result) == 0


def test_transaction_descriptions_basic():
    """Минимальный тест transaction_descriptions"""
    from generators import transaction_descriptions

    result = list(transaction_descriptions(SAMPLE_TRANSACTIONS))
    assert result == ["Payment 1", "Payment 2", "Payment 3", "No amount"]


def test_card_number_generator_basic():
    """Минимальный тест card_number_generator"""
    from generators import card_number_generator

    result = list(card_number_generator(1, 3))
    assert result == ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]


def test_card_number_generator_error():
    """Тест ошибки генератора"""
    from generators import card_number_generator

    with pytest.raises(ValueError):
        list(card_number_generator(10, 5))
