import pytest
from unittest.mock import patch, MagicMock
import os
from src.external_api import get_exchange_rate, get_transaction_amount_in_rub


@patch.dict(os.environ, {'EXCHANGE_RATE_API_KEY': 'test_api_key'})
@patch('src.external_api.requests.get')
def test_get_exchange_rate_success(mock_get):
    """Тест успешного получения курса валют."""
    # Мокаем ответ API
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'success': True,
        'rates': {'RUB': 75.5}
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    rate = get_exchange_rate('USD', 'RUB')

    assert rate == 75.5
    mock_get.assert_called_once()


@patch.dict(os.environ, {'EXCHANGE_RATE_API_KEY': 'test_api_key'})
@patch('src.external_api.requests.get')
def test_get_exchange_rate_api_error(mock_get):
    """Тест ошибки API."""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'success': False,
        'error': {'info': 'Invalid API key'}
    }
    mock_get.return_value = mock_response

    with pytest.raises(ValueError, match="Ошибка API"):
        get_exchange_rate('USD', 'RUB')


def test_get_exchange_rate_no_api_key():
    """Тест отсутствия API ключа."""
    # Патчим переменную API_KEY напрямую в модуле external_api
    with patch('src.external_api.API_KEY', None):
        with pytest.raises(ValueError, match="API ключ не найден"):
            get_exchange_rate('USD', 'RUB')


@patch('src.external_api.get_exchange_rate')
def test_get_transaction_amount_in_rub_rub(mock_get_rate):
    """Тест транзакции в рублях (без конвертации)."""
    transaction = {
        'amount': '100.0',
        'currency': 'RUB'
    }

    result = get_transaction_amount_in_rub(transaction)

    assert result == 100.0
    mock_get_rate.assert_not_called()  # API не должно вызываться


@patch('src.external_api.get_exchange_rate')
def test_get_transaction_amount_in_rub_usd(mock_get_rate):
    """Тест транзакции в USD с конвертацией."""
    # Настраиваем мок для возврата курса
    mock_get_rate.return_value = 75.5

    transaction = {
        'amount': '50.0',
        'currency': 'USD'
    }

    result = get_transaction_amount_in_rub(transaction)

    assert result == 50.0 * 75.5
    mock_get_rate.assert_called_once_with('USD', 'RUB')


@patch('src.external_api.get_exchange_rate')
def test_get_transaction_amount_in_rub_eur(mock_get_rate):
    """Тест транзакции в EUR с конвертацией."""
    mock_get_rate.return_value = 85.0

    transaction = {
        'amount': '30.0',
        'currency': 'EUR'
    }

    result = get_transaction_amount_in_rub(transaction)

    assert result == 30.0 * 85.0
    mock_get_rate.assert_called_once_with('EUR', 'RUB')


def test_get_transaction_amount_missing_fields():
    """Тест транзакции без обязательных полей."""
    transaction = {'id': 1}  # Нет amount и currency

    with pytest.raises(KeyError):
        get_transaction_amount_in_rub(transaction)


def test_get_transaction_amount_unsupported_currency():
    """Тест транзакции с неподдерживаемой валютой."""
    transaction = {
        'amount': '100.0',
        'currency': 'GBP'  # Не поддерживается
    }

    # Вариант 1: Проверяем точное сообщение
    with pytest.raises(ValueError, match="Неподдерживаемая валюта: GBP"):
        get_transaction_amount_in_rub(transaction)


@patch('src.external_api.get_exchange_rate', side_effect=ConnectionError("API error"))
def test_get_transaction_amount_api_error(mock_get_rate):
    """Тест ошибки при обращении к API."""
    transaction = {
        'amount': '50.0',
        'currency': 'USD'
    }

    with pytest.raises(ConnectionError):
        get_transaction_amount_in_rub(transaction)