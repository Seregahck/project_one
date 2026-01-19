import json
import os
from typing import Any, Dict, List


def load_transactions(file_path: str = "data/operations.json") -> List[Dict[str, Any]]:
    """
    Загружает транзакции из JSON-файла.

    Args:
        file_path: Путь до JSON-файла (по умолчанию "data/operations.json")

    Returns:
        Список словарей с данными о транзакциях
    """
    try:
        # Проверяем существование файла
        if not os.path.exists(file_path):
            return []

        # Проверяем, что файл не пустой
        if os.path.getsize(file_path) == 0:
            return []

        # Открываем и читаем файл
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Проверяем, что данные - это список
        if not isinstance(data, list):
            return []

        return data

    except (json.JSONDecodeError, IOError):
        return []
