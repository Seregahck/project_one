import pytest
from datetime import datetime, timedelta
import random


# Фикстуры для общих тестовых данных
@pytest.fixture
def sample_transactions():
    """Базовый набор транзакций"""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-15T10:30:00.000", "amount": 100},
        {"id": 2, "state": "PENDING", "date": "2023-02-20T14:45:00.000", "amount": 200},
        {"id": 3, "state": "EXECUTED", "date": "2023-03-10T09:15:00.000", "amount": 300},
        {"id": 4, "state": "CANCELED", "date": "2023-04-05T16:20:00.000", "amount": 400},
        {"id": 5, "state": "EXECUTED", "date": "2023-05-12T11:10:00.000", "amount": 500},
    ]


@pytest.fixture
def empty_transactions():
    """Пустой список транзакций"""
    return []


@pytest.fixture
def single_transaction():
    """Одна транзакция"""
    return [{"id": 1, "state": "EXECUTED", "date": "2023-01-01T12:00:00.000", "amount": 1000}]


# Фикстуры с различными комбинациями state
@pytest.fixture
def only_executed_transactions():
    """Только EXECUTED транзакции"""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-01", "amount": 100},
        {"id": 2, "state": "EXECUTED", "date": "2023-01-02", "amount": 200},
        {"id": 3, "state": "EXECUTED", "date": "2023-01-03", "amount": 300},
    ]


@pytest.fixture
def only_pending_transactions():
    """Только PENDING транзакции"""
    return [
        {"id": 1, "state": "PENDING", "date": "2023-02-01", "amount": 50},
        {"id": 2, "state": "PENDING", "date": "2023-02-02", "amount": 150},
        {"id": 3, "state": "PENDING", "date": "2023-02-03", "amount": 250},
    ]


@pytest.fixture
def mixed_state_transactions():
    """Смешанные состояния без EXECUTED"""
    return [
        {"id": 1, "state": "PENDING", "date": "2023-03-01", "amount": 100},
        {"id": 2, "state": "CANCELED", "date": "2023-03-02", "amount": 200},
        {"id": 3, "state": "FAILED", "date": "2023-03-03", "amount": 300},
    ]


@pytest.fixture
def transactions_without_state():
    """Транзакции без ключа state"""
    return [
        {"id": 1, "date": "2023-01-01", "amount": 100},
        {"id": 2, "state": None, "date": "2023-01-02", "amount": 200},
        {"id": 3, "state": "", "date": "2023-01-03", "amount": 300},
        {"id": 4, "state": "EXECUTED", "date": "2023-01-04", "amount": 400},
    ]


# Фикстуры с различными комбинациями date
@pytest.fixture
def chronological_transactions():
    """Транзакции в хронологическом порядке"""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2022-12-01T10:00:00.000", "amount": 100},
        {"id": 2, "state": "EXECUTED", "date": "2023-01-15T11:30:00.000", "amount": 200},
        {"id": 3, "state": "EXECUTED", "date": "2023-03-10T09:15:00.000", "amount": 300},
        {"id": 4, "state": "EXECUTED", "date": "2023-05-20T16:45:00.000", "amount": 400},
    ]


@pytest.fixture
def reverse_chronological_transactions():
    """Транзакции в обратном хронологическом порядке"""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-05-20T16:45:00.000", "amount": 400},
        {"id": 2, "state": "EXECUTED", "date": "2023-03-10T09:15:00.000", "amount": 300},
        {"id": 3, "state": "EXECUTED", "date": "2023-01-15T11:30:00.000", "amount": 200},
        {"id": 4, "state": "EXECUTED", "date": "2022-12-01T10:00:00.000", "amount": 100},
    ]


@pytest.fixture
def same_date_transactions():
    """Транзакции с одинаковыми датами"""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-01T10:00:00.000", "amount": 100},
        {"id": 2, "state": "PENDING", "date": "2023-01-01T11:00:00.000", "amount": 200},
        {"id": 3, "state": "CANCELED", "date": "2023-01-01T12:00:00.000", "amount": 300},
        {"id": 4, "state": "EXECUTED", "date": "2023-01-01T13:00:00.000", "amount": 400},
    ]


@pytest.fixture
def different_date_formats():
    """Транзакции с разными форматами дат"""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-01"},  # только дата
        {"id": 2, "state": "EXECUTED", "date": "2023-01-01T10:30:00"},  # дата и время
        {"id": 3, "state": "EXECUTED", "date": "2023-01-01T10:30:00.000"},  # с миллисекундами
        {"id": 4, "state": "EXECUTED", "date": "2023-01-01T10:30:00Z"},  # с часовым поясом
        {"id": 5, "state": "EXECUTED", "date": "2023-01-01T10:30:00+03:00"},  # с offset
    ]


@pytest.fixture
def transactions_without_date():
    """Транзакции без ключа date"""
    return [
        {"id": 1, "state": "EXECUTED", "amount": 100},
        {"id": 2, "state": "EXECUTED", "date": None, "amount": 200},
        {"id": 3, "state": "EXECUTED", "date": "", "amount": 300},
        {"id": 4, "state": "EXECUTED", "date": "2023-01-01", "amount": 400},
    ]


@pytest.fixture
def invalid_date_transactions():
    """Транзакции с невалидными датами"""
    return [
        {"id": 1, "state": "EXECUTED", "date": "not-a-date", "amount": 100},
        {"id": 2, "state": "EXECUTED", "date": "2023-13-01", "amount": 200},  # несуществующий месяц
        {"id": 3, "state": "EXECUTED", "date": "2023-12-32", "amount": 300},  # несуществующий день
        {"id": 4, "state": "EXECUTED", "date": "2023-01-01", "amount": 400},  # валидная
    ]


# Комбинированные фикстуры
@pytest.fixture
def transactions_state_date_combinations():
    """Различные комбинации state и date"""
    return [
        # Разные состояния, разные даты
        {"id": 1, "state": "EXECUTED", "date": "2023-01-01", "amount": 100},
        {"id": 2, "state": "PENDING", "date": "2023-01-02", "amount": 200},
        {"id": 3, "state": "EXECUTED", "date": "2023-01-03", "amount": 300},
        {"id": 4, "state": "CANCELED", "date": "2023-01-04", "amount": 400},
        # Одинаковые состояния, разные даты
        {"id": 5, "state": "EXECUTED", "date": "2023-02-01", "amount": 500},
        {"id": 6, "state": "EXECUTED", "date": "2023-02-02", "amount": 600},
        # Разные состояния, одинаковые даты
        {"id": 7, "state": "EXECUTED", "date": "2023-03-01", "amount": 700},
        {"id": 8, "state": "PENDING", "date": "2023-03-01", "amount": 800},
        {"id": 9, "state": "CANCELED", "date": "2023-03-01", "amount": 900},
    ]


@pytest.fixture
def large_dataset():
    """Большой набор данных для тестирования производительности"""
    transactions = []
    start_date = datetime(2023, 1, 1)

    for i in range(100):
        # Чередуем состояния
        if i % 3 == 0:
            state = "EXECUTED"
        elif i % 3 == 1:
            state = "PENDING"
        else:
            state = "CANCELED"

        # Случайная дата в пределах года
        random_date = start_date + timedelta(days=random.randint(0, 364))

        transactions.append({
            "id": i + 1,
            "state": state,
            "date": random_date.isoformat(),
            "amount": random.randint(10, 10000),
            "description": f"Transaction {i + 1}"
        })

    return transactions


# Параметризованные фикстуры
@pytest.fixture(params=["EXECUTED", "PENDING", "CANCELED"])
def single_state_transactions(request):
    """Транзакции с одним состоянием (параметризованная)"""
    return [
        {"id": 1, "state": request.param, "date": "2023-01-01", "amount": 100},
        {"id": 2, "state": request.param, "date": "2023-01-02", "amount": 200},
        {"id": 3, "state": request.param, "date": "2023-01-03", "amount": 300},
    ]


@pytest.fixture(params=[True, False])
def sort_direction(request):
    """Направление сортировки (параметризованная)"""
    return request.param


# Фикстура для edge cases
@pytest.fixture
def edge_case_transactions():
    """Крайние случаи"""
    return [
        # Пустые значения
        {"id": 1, "state": "", "date": "", "amount": 100},
        {"id": 2, "state": None, "date": None, "amount": 200},
        # Очень старые/новые даты
        {"id": 3, "state": "EXECUTED", "date": "2000-01-01", "amount": 300},
        {"id": 4, "state": "EXECUTED", "date": "2100-12-31", "amount": 400},
        # Специальные символы
        {"id": 5, "state": "EXECUTED", "date": "2023-01-01T00:00:00.000", "amount": 500},
        # Минимальные/максимальные значения
        {"id": 6, "state": "EXECUTED", "date": "2023-01-01", "amount": 0},
        {"id": 7, "state": "EXECUTED", "date": "2023-01-01", "amount": 9999999},
    ]


# Фикстуры для конкретных функций тестирования
@pytest.fixture
def filter_test_data():
    """Данные специально для тестирования фильтрации"""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-01", "should_be_filtered": True},
        {"id": 2, "state": "PENDING", "date": "2023-01-02", "should_be_filtered": False},
        {"id": 3, "state": "EXECUTED", "date": "2023-01-03", "should_be_filtered": True},
        {"id": 4, "state": "", "date": "2023-01-04", "should_be_filtered": False},
        {"id": 5, "state": None, "date": "2023-01-05", "should_be_filtered": False},
    ]


@pytest.fixture
def sort_test_data():
    """Данные специально для тестирования сортировки"""
    return [
        {"id": 3, "date": "2023-03-01"},
        {"id": 1, "date": "2023-01-01"},
        {"id": 4, "date": "2023-04-01"},
        {"id": 2, "date": "2023-02-01"},
        # Ожидаемый порядок: id 1, 2, 3, 4
    ]