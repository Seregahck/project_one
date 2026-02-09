import re
from collections import Counter
from datetime import datetime
from typing import List, Dict, Optional


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
        description = transaction.get('description', '')
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
        description = transaction.get('description', '')
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