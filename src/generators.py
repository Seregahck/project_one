def filter_by_currency(transactions: list, currency_code: str):
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


