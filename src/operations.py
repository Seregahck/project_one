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