from typing import Any, Dict, Generator, Iterator, List


def filter_by_currency(transactions: List[Dict[str, Any]], currency_code: str) -> Iterator[Dict[str, Any]]:
    """
    Фильтрует транзакции по заданной валюте.

    Args:
        transactions (list): Список словарей с транзакциями
        currency_code (str): Код валюты для фильтрации (например, "USD")

    Yields:
        dict: Транзакции, где валюта операции соответствует заданной
    """
    for transaction in transactions:
        # Проверяем, есть ли ключ operationAmount и корректная структура currency
        operation_amount = transaction.get("operationAmount", {})
        currency = operation_amount.get("currency", {})
        if currency.get("code") == currency_code:
            yield transaction


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """
    Генерирует описания транзакций.

    Args:
        transactions (list): Список словарей с транзакциями

    Yields:
        str: Описание каждой транзакции
    """
    for transaction in transactions:
        description = transaction.get("description", "")
        yield description


def card_number_generator(start: int, stop: int) -> Generator[str, None, None]:
    """
    Генерирует номера банковских карт в заданном диапазоне.

    Args:
        start (int): Начальный номер карты (от 1)
        stop (int): Конечный номер карты (до 9999999999999999)

    Yields:
        str: Номер карты в формате "XXXX XXXX XXXX XXXX"

    Raises:
        ValueError: Если start или stop вне допустимого диапазона
    """
    # Проверяем диапазон
    if start < 1 or stop > 9999999999999999:
        raise ValueError("Диапазон должен быть от 1 до 9999999999999999")
    if start > stop:
        raise ValueError("Начальное значение должно быть меньше или равно конечному")

    for number in range(start, stop + 1):
        # Форматируем число в 16-значную строку с ведущими нулями
        card_number_str = f"{number:016d}"

        # Разбиваем на группы по 4 цифры
        formatted_number = (
            f"{card_number_str[0:4]} {card_number_str[4:8]} {card_number_str[8:12]} {card_number_str[12:16]}"
        )

        yield formatted_number
