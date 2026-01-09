import pytest


from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


# Фикстура для тестовых данных
@pytest.fixture
def sample_transactions():
    """Фикстура с тестовыми данными транзакций"""
    return [
        {"id": 1, "operationAmount": {"currency": {"code": "USD"}}, "description": "Payment 1"},
        {"id": 2, "operationAmount": {"currency": {"code": "EUR"}}, "description": "Payment 2"},
        {"id": 3, "operationAmount": {"currency": {"code": "USD"}}, "description": "Payment 3"},
        {"description": "No amount"}  # Транзакция без operationAmount
    ]


# Параметризованные тесты для filter_by_currency
@pytest.mark.parametrize("currency_code,expected_count,expected_ids", [
    ("USD", 2, [1, 3]),
    ("EUR", 1, [2]),
    ("GBP", 0, []),
    ("RUB", 0, []),
])
def test_filter_by_currency(sample_transactions, currency_code, expected_count, expected_ids):
    """Параметризованный тест filter_by_currency"""
    result = list(filter_by_currency(sample_transactions, currency_code))

    assert len(result) == expected_count
    assert [t["id"] for t in result if "id" in t] == expected_ids

    # Проверяем, что у всех найденных транзакций правильная валюта
    for transaction in result:
        assert transaction["operationAmount"]["currency"]["code"] == currency_code


def test_filter_by_currency_empty_input():
    """Тест с пустым списком транзакций"""
    result = list(filter_by_currency([], "USD"))
    assert len(result) == 0


def test_filter_by_currency_no_operation_amount(sample_transactions):
    """Тест обработки транзакций без operationAmount"""
    # Добавляем транзакцию без operationAmount
    transactions_with_missing = sample_transactions + [{"id": 99, "description": "No amount at all"}]

    result = list(filter_by_currency(transactions_with_missing, "USD"))
    # Должны найти только транзакции 1 и 3
    assert len(result) == 2
    assert [t["id"] for t in result] == [1, 3]


# Тесты для transaction_descriptions
def test_transaction_descriptions_basic(sample_transactions):
    """Тест transaction_descriptions"""
    result = list(transaction_descriptions(sample_transactions))
    assert result == ["Payment 1", "Payment 2", "Payment 3", "No amount"]


def test_transaction_descriptions_empty():
    """Тест с пустым списком"""
    result = list(transaction_descriptions([]))
    assert result == []


def test_transaction_descriptions_no_description():
    """Тест с транзакциями без описания"""
    transactions = [
        {"id": 1},
        {"id": 2, "description": "Test"},
        {"id": 3, "description": ""},
    ]
    result = list(transaction_descriptions(transactions))
    assert result == [None, "Test", ""]


# Параметризованные тесты для card_number_generator
@pytest.mark.parametrize("start,end,expected", [
    (1, 3, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]),
    (9999999999999997, 9999999999999999, [
        "9999 9999 9999 9997",
        "9999 9999 9999 9998",
        "9999 9999 9999 9999"
    ]),
    (5, 5, ["0000 0000 0000 0005"]),  # Один элемент
    (1, 1, ["0000 0000 0000 0001"]),  # Начало диапазона
])
def test_card_number_generator(start, end, expected):
    """Параметризованный тест card_number_generator"""
    result = list(card_number_generator(start, end))
    assert result == expected

    # Проверяем формат каждого номера
    for card_number in result:
        assert len(card_number) == 19  # 16 цифр + 3 пробела
        assert card_number.count(" ") == 3
        # Проверяем, что после удаления пробелов это число
        assert card_number.replace(" ", "").isdigit()


@pytest.mark.parametrize("start,end", [
    (10, 5),  # start > end
    (-1, 5),  # отрицательное число
    (0, 0),  # ноль
    (10000000000000000, 10000000000000001),  # больше 16 цифр
])
def test_card_number_generator_errors(start, end):
    """Тест ошибок card_number_generator"""
    with pytest.raises(ValueError, match=".*"):
        list(card_number_generator(start, end))


def test_card_number_generator_format():
    """Тест формата номеров карт"""
    # Проверяем форматирование с ведущими нулями
    result = list(card_number_generator(123, 123))
    assert result[0] == "0000 0000 0000 0123"

    result = list(card_number_generator(1, 2))
    assert result == ["0000 0000 0000 0001", "0000 0000 0000 0002"]


# Тест на большие диапазоны (генератор должен быть ленивым)
def test_card_number_generator_large_range():
    """Тест, что генератор ленивый и работает с большими диапазонами"""
    generator = card_number_generator(1, 1000000)
    first_five = []
    for i, num in enumerate(generator):
        if i >= 5:
            break
        first_five.append(num)

    assert first_five == [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005",
    ]
