import csv
from typing import List, Dict, Any
import pandas as pd


def read_csv_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает финансовые операции из CSV файла.

    Args:
        file_path (str): Путь к CSV файлу

    Returns:
        List[Dict[str, Any]]: Список словарей с транзакциями
    """
    transactions = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Используем DictReader для автоматического создания словарей
            csv_reader = csv.DictReader(file)

            # Преобразуем каждую строку в словарь
            for row in csv_reader:
                transactions.append(dict(row))

    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {file_path} не найден")
    except Exception as e:
        raise Exception(f"Ошибка при чтении CSV файла: {str(e)}")

    return transactions


def read_excel_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает финансовые операции из Excel файла.

    Args:
        file_path (str): Путь к Excel файлу

    Returns:
        List[Dict[str, Any]]: Список словарей с транзакциями
    """
    try:
        # Читаем Excel файл
        df = pd.read_excel(file_path)

        # Преобразуем DataFrame в список словарей
        transactions = df.to_dict('records')

        return transactions

    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {file_path} не найден")
    except Exception as e:
        raise Exception(f"Ошибка при чтении Excel файла: {str(e)}")
