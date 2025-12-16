from typing import Dict, List


def filter_by_state(transactions: List[Dict], state: str = "EXECUTED") -> List[Dict]:
    """Фильтрует список транзакций по статусу выполнения."""
    # Используем list comprehension для более читаемого кода
    return [transaction for transaction in transactions if transaction.get("state") == state]


def sort_by_date(transactions: List[Dict], reverse: bool = True) -> List[Dict]:
    """Сортирует список словарей по дате (по умолчанию - по убыванию)."""
    return sorted(transactions, key=lambda x: x["date"], reverse=reverse)


# Тестовые данные
transactions = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]

# Тестирование
print("Отфильтрованные транзакции (EXECUTED):")
filtered = filter_by_state(transactions, "EXECUTED")
for transaction in filtered:
    print(f"  ID: {transaction['id']}, Дата: {transaction['date']}")

print("\nСортированные по дате (по убыванию):")
sorted_transactions = sort_by_date(filtered)
for transaction in sorted_transactions:
    print(f"  ID: {transaction['id']}, Дата: {transaction['date']}")

print("\nСортированные по дате (по возрастанию):")
sorted_asc = sort_by_date(filtered, reverse=False)
for transaction in sorted_asc:
    print(f"  ID: {transaction['id']}, Дата: {transaction['date']}")
