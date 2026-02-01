import csv
from typing import Any, Dict, List, Union, cast

import numpy as np
import pandas as pd


def read_csv_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает финансовые операции из CSV файла.

    Args:
        file_path: Путь к CSV файлу

    Returns:
        Список словарей с транзакциями

    Raises:
        FileNotFoundError: Если файл не найден
        ValueError: Если файл пуст или имеет некорректный формат
    """
    transactions: List[Dict[str, Any]] = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            # Проверяем, что файл не пустой
            if reader.fieldnames is None:
                raise ValueError("CSV файл пуст или не содержит заголовков")

            for row in reader:
                # Преобразуем пустые строки в None
                cleaned_row: Dict[str, Any] = {key: (value if value != "" else None) for key, value in row.items()}
                transactions.append(cleaned_row)

    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {file_path}")
    except Exception as e:
        raise ValueError(f"Ошибка при чтении CSV файла: {str(e)}")

    if not transactions:
        raise ValueError("CSV файл не содержит данных")

    return transactions


def read_excel_transactions(file_path: str, sheet_name: Union[str, int] = 0) -> List[Dict[str, Any]]:
    """
    Читает финансовые операции из Excel файла.

    Args:
        file_path: Путь к Excel файлу
        sheet_name: Название или индекс листа (по умолчанию первый лист)

    Returns:
        Список словарей с транзакциями

    Raises:
        FileNotFoundError: Если файл не найден
        ValueError: Если файл пуст или имеет некорректный формат
    """
    try:
        # Читаем Excel файл
        df: pd.DataFrame = pd.read_excel(file_path, sheet_name=sheet_name)

        # Проверяем, что DataFrame не пустой
        if df.empty:
            raise ValueError("Excel файл пуст")

        # Преобразуем NaN/NaT в None
        df = df.replace([np.nan, pd.NaT], None)

        # Преобразуем DataFrame в список словарей
        # Используем cast для преобразования типов
        raw_transactions = df.to_dict("records")
        transactions: List[Dict[str, Any]] = cast(List[Dict[str, Any]], raw_transactions)

        return transactions

    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {file_path}")
    except Exception as e:
        raise ValueError(f"Ошибка при чтении Excel файла: {str(e)}")
