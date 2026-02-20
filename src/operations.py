import re
from collections import Counter
from datetime import datetime
from typing import Dict, List


def process_bank_search(data: List[Dict], search: str) -> List[Dict]:
    """
    Ищет транзакции по строке в описании с использованием регулярных выражений.

    Args:
        data: Список словарей с данными о банковских операциях
        search: Строка для поиска в описании

    Returns:
        Список словарей с операциями, содержащими строку поиска в описании
    """
    if not data or not search:
        return []

    try:
        pattern = re.compile(search, re.IGNORECASE)
    except re.error:
        # В случае невалидного регулярного выражения
        pattern = None

    result = []
    for transaction in data:
        description = transaction.get("description", "")
        if not description:
            continue

        if pattern and pattern.search(description):
            result.append(transaction)
        elif pattern is None and search.lower() in description.lower():
            # Простое сравнение, если регулярное выражение невалидно
            result.append(transaction)

    return result


def process_bank_operations(data: List[Dict], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество операций по категориям.

    Args:
        data: Список словарей с данными о банковских операциях
        categories: Список категорий операций для подсчета

    Returns:
        Словарь с количеством операций по категориям
    """
    if not data:
        return {}

    # Извлекаем все описания
    descriptions = []
    for transaction in data:
        description = transaction.get("description", "")
        if description:
            descriptions.append(description)

    # Считаем количество каждого описания
    counter = Counter(descriptions)

    # Создаем результат для запрошенных категорий
    result = {}
    for category in categories:
        category_lower = category.lower()
        total = 0
        for desc, count in counter.items():
            if category_lower in desc.lower():
                total += count
        result[category] = total

    return result


def filter_by_status(data: List[Dict], status: str) -> List[Dict]:
    """
    Фильтрует транзакции по статусу.

    Args:
        data: Список транзакций
        status: Статус для фильтрации

    Returns:
        Отфильтрованный список транзакций
    """
    if not data:
        return []

    status_upper = status.upper()
    return [t for t in data if t.get("state", "").upper() == status_upper]


def sort_transactions(data: List[Dict], reverse: bool = False) -> List[Dict]:
    """
    Сортирует транзакции по дате.

    Args:
        data: Список транзакций
        reverse: Если True - по убыванию, иначе по возрастанию

    Returns:
        Отсортированный список транзакций
    """

    def get_date(transaction: Dict) -> datetime:
        date_str = transaction.get("date", "")
        try:
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            return datetime.min

    return sorted(data, key=get_date, reverse=reverse)


def filter_rub_transactions(data: List[Dict]) -> List[Dict]:
    """
    Фильтрует только рублевые транзакции.

    Args:
        data: Список транзакций

    Returns:
        Список рублевых транзакций
    """
    return [t for t in data if t.get("operationAmount", {}).get("currency", {}).get("code") == "RUB"]


def mask_account_number(account: str) -> str:
    """
    Маскирует номер счета или карты.

    Args:
        account: Номер счета или карты

    Returns:
        Замаскированный номер
    """
    if not account:
        return ""

    # Обработка счета
    if "Счет" in account:
        numbers = "".join(filter(str.isdigit, account))
        if len(numbers) >= 4:
            return f"Счет **{numbers[-4:]}"
        return account

    # Обработка карты
    parts = account.split()
    if len(parts) >= 2:
        name = " ".join(parts[:-1])
        number = parts[-1]
        digits = "".join(filter(str.isdigit, number))

        if len(digits) == 16:
            masked = f"{digits[:4]} {digits[4:6]}** **** {digits[-4:]}"
            return f"{name} {masked}"

    return account


def format_transaction(transaction: Dict) -> str:
    """
    Форматирует транзакцию для вывода.

    Args:
        transaction: Словарь с данными транзакции

    Returns:
        Отформатированная строка
    """
    # Форматирование даты
    date_str = transaction.get("date", "")
    try:
        date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        formatted_date = date.strftime("%d.%m.%Y")
    except (ValueError, AttributeError):
        formatted_date = "Дата не указана"

    description = transaction.get("description", "Без описания")

    # Форматирование отправителя и получателя
    from_account = mask_account_number(transaction.get("from", ""))
    to_account = mask_account_number(transaction.get("to", ""))

    # Форматирование суммы
    amount_data = transaction.get("operationAmount", {})
    amount = amount_data.get("amount", "0")
    currency = amount_data.get("currency", {}).get("name", "руб.")

    result_lines = [f"{formatted_date} {description}"]

    if from_account and to_account:
        result_lines.append(f"{from_account} -> {to_account}")
    elif from_account:
        result_lines.append(f"{from_account}")
    elif to_account:
        result_lines.append(f"{to_account}")

    result_lines.append(f"Сумма: {amount} {currency}\n")

    return "\n".join(result_lines)


def load_json_transactions(filename: str) -> List[Dict]:
    """
    Загружает транзакции из JSON файла.

    Args:
        filename: Имя файла

    Returns:
        Список транзакций
    """
    import json
    from typing import Dict, List

    try:
        with open(filename, "r", encoding="utf-8") as f:
            result: List[Dict] = json.load(f)
            return result
    except (FileNotFoundError, json.JSONDecodeError):
        empty_result: List[Dict] = []
        return empty_result
