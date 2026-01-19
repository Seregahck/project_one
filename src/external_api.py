import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

API_KEY = os.getenv('EXCHANGE_RATE_API_KEY')
BASE_URL = "https://apilayer.com/exchangerates_data-api"


def get_exchange_rate(from_currency: str, to_currency: str = 'RUB') -> float:
    """
    Получает курс обмена валют через внешнее API.

    Args:
        from_currency: Исходная валюта (USD, EUR и т.д.)
        to_currency: Целевая валюта (по умолчанию RUB)

    Returns:
        Курс обмена

    Raises:
        Exception: Если произошла ошибка при получении курса
    """
    if not API_KEY:
        raise ValueError("API ключ не найден. Проверьте файл .env")

    url = f"{BASE_URL}/latest"
    params = {
        'base': from_currency,
        'symbols': to_currency
    }
    headers = {
        'apikey': API_KEY
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data.get('success', False):
            raise ValueError(f"Ошибка API: {data.get('error', {}).get('info', 'Unknown error')}")

        return float(data['rates'][to_currency])

    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Ошибка подключения к API: {str(e)}")
    except KeyError as e:
        raise ValueError(f"Неожиданный формат ответа API: отсутствует ключ {e}")


def get_transaction_amount_in_rub(transaction: Dict[str, Any]) -> float:
    """
    Возвращает сумму транзакции в рублях.

    Args:
        transaction: Словарь с данными о транзакции

    Returns:
        Сумма в рублях (тип float)

    Raises:
        KeyError: Если в транзакции отсутствуют обязательные поля
        ValueError: Если валюта не поддерживается
    """
    # Проверяем обязательные поля
    required_fields = ['amount', 'currency']
    for field in required_fields:
        if field not in transaction:
            raise KeyError(f"Отсутствует обязательное поле: {field}")

    amount = float(transaction['amount'])
    currency = transaction['currency'].upper()

    # Если уже рубли, возвращаем как есть
    if currency == 'RUB':
        return amount

    # Если USD или EUR, конвертируем
    if currency in ['USD', 'EUR']:
        rate = get_exchange_rate(currency, 'RUB')
        return amount * rate

    # Если валюта не поддерживается - вызываем исключение
    raise ValueError(f"Неподдерживаемая валюта: {currency}")
