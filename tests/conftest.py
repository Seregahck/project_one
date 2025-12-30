import pytest

# 1. Фикстуры для тестов get_mask_card_number

@pytest.fixture
def valid_card_numbers():
    """Валидные номера карт для тестирования"""
    return [
        "1234567890123456",
        "1111222233334444",
        "0000000000000000",
        "0123456789012345",
    ]


@pytest.fixture
def invalid_card_numbers():
    """Невалидные номера карт"""
    return [
        ("123", "Номер карты должен состоять из 16 цифр."),  # слишком короткий
        ("12345678901234567", "Номер карты должен состоять из 16 цифр."),  # слишком длинный
        ("1234abcd90123456", "Номер карты должен содержать только цифры"),  # содержит буквы
        ("1234-5678-9012-3456", "Номер карты должен содержать только цифры"),  # содержит тире
        ("", "Номер карты должен содержать только цифры"),  # пустая строка
    ]


@pytest.fixture
def card_numbers_with_spaces():
    """Номера карт с пробелами"""
    return [
        "1234 5678 9012 3456",
        " 1234567890123456 ",
        "1234  5678  9012  3456",
    ]


# 2. Фикстуры для тестов get_mask_account

@pytest.fixture
def valid_account_numbers():
    """Валидные номера счетов"""
    return [
        "40817810570012345678",
        "1234",  # минимальная длина
        "5678",
        "1234567890",
    ]


@pytest.fixture
def invalid_account_numbers():
    """Невалидные номера счетов"""
    return [
        ("123", "Номер счета должен быть длиной не менее 4 цифр"),  # слишком короткий
        ("12", "Номер счета должен быть длиной не менее 4 цифр"),  # слишком короткий
        ("1", "Номер счета должен быть длиной не менее 4 цифр"),  # слишком короткий
        ("1234-abcd", "Номер счета должен содержать только цифры"),  # содержит тире и буквы
        ("", "Номер счета должен содержать только цифры"),  # пустая строка
    ]


@pytest.fixture
def account_numbers_with_spaces():
    """Номера счетов с пробелами"""
    return [
        "4081 7810 5700 1234 5678",
        " 1234 ",
        "12 34",
    ]


# 3. Фикстуры для тестов mask_account_card

@pytest.fixture
def card_strings():
    """Строки с картами для mask_account_card"""
    return [
        "Visa 1234567890123456",
        "MasterCard 1111222233334444",
        "МИР 0123456789012345",
    ]


@pytest.fixture
def account_strings():
    """Строки со счетами для mask_account_card"""
    return [
        "Счет 40817810570012345678",
        "СЧЕТ 12345678901234567890",
        "счет 1234",
    ]


@pytest.fixture
def edge_strings():
    """Крайние случаи для mask_account_card"""
    return [
        "",  # пустая строка
        "   ",  # только пробелы
        "Visa",  # только тип
        "Счет",  # только тип
        "Visa 123",  # слишком короткий номер
    ]


# 4. Фикстуры для тестов get_date

@pytest.fixture
def valid_dates():
    """Валидные даты"""
    return [
        "2023-12-31",
        "2024-02-29",  # високосный год
        "2023-01-01",
    ]


@pytest.fixture
def invalid_dates():
    """Невалидные даты"""
    return [
        "",  # пустая строка
        "not-a-date",  # не дата
        "31.12.2023",  # обратный формат
        "2023-13-01",  # несуществующий месяц
    ]


# 5. Фикстуры для тестов filter_by_state

@pytest.fixture
def sample_transactions():
    """Образец транзакций"""
    return [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "PENDING"},
        {"id": 3, "state": "EXECUTED"},
        {"id": 4, "state": "CANCELED"},
    ]


@pytest.fixture
def executed_transactions():
    """Только EXECUTED транзакции"""
    return [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "EXECUTED"},
        {"id": 3, "state": "EXECUTED"},
    ]


@pytest.fixture
def pending_transactions():
    """Только PENDING транзакции"""
    return [
        {"id": 1, "state": "PENDING"},
        {"id": 2, "state": "PENDING"},
    ]


@pytest.fixture
def empty_transactions():
    """Пустой список транзакций"""
    return []


@pytest.fixture
def single_transaction():
    """Одна транзакция"""
    return [{"id": 1, "state": "EXECUTED"}]


# 6. Фикстуры для тестов sort_by_date

@pytest.fixture
def dated_transactions():
    """Транзакции с датами"""
    return [
        {"id": 1, "date": "2023-01-01"},
        {"id": 2, "date": "2023-12-31"},
        {"id": 3, "date": "2023-06-15"},
    ]


@pytest.fixture
def chronological_transactions():
    """Транзакции в хронологическом порядке"""
    return [
        {"id": 1, "date": "2022-12-01"},
        {"id": 2, "date": "2023-01-15"},
        {"id": 3, "date": "2023-03-10"},
        {"id": 4, "date": "2023-05-20"},
    ]


@pytest.fixture
def same_date_transactions():
    """Транзакции с одинаковыми датами"""
    return [
        {"id": 1, "date": "2023-01-01"},
        {"id": 2, "date": "2023-01-01"},
        {"id": 3, "date": "2023-01-01"},
    ]
