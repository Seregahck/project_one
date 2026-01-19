import json
import os
import tempfile
import pytest
from unittest.mock import mock_open, patch
from src.utils import load_transactions


def test_load_transactions_valid_file():
    """Тест загрузки корректного JSON-файла."""
    # Создаем временный файл с тестовыми данными
    test_data = [
        {"id": 1, "amount": 100.0, "currency": "RUB"},
        {"id": 2, "amount": 50.0, "currency": "USD"}
    ]

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(test_data, f)
        temp_path = f.name

    try:
        result = load_transactions(temp_path)
        assert result == test_data
    finally:
        os.unlink(temp_path)


def test_load_transactions_empty_file():
    """Тест загрузки пустого файла."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_path = f.name

    try:
        result = load_transactions(temp_path)
        assert result == []
    finally:
        os.unlink(temp_path)


def test_load_transactions_file_not_found():
    """Тест случая, когда файл не существует."""
    result = load_transactions('/nonexistent/path/file.json')
    assert result == []


def test_load_transactions_not_list():
    """Тест случая, когда JSON не является списком."""
    test_data = {"id": 1, "amount": 100.0}

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(test_data, f)
        temp_path = f.name

    try:
        result = load_transactions(temp_path)
        assert result == []
    finally:
        os.unlink(temp_path)


def test_load_transactions_invalid_json():
    """Тест случая с некорректным JSON."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write('{ invalid json }')
        temp_path = f.name

    try:
        result = load_transactions(temp_path)
        assert result == []
    finally:
        os.unlink(temp_path)


@patch('builtins.open', side_effect=IOError("File read error"))
def test_load_transactions_io_error(mock_file):
    """Тест обработки ошибок ввода-вывода."""
    result = load_transactions('/some/path.json')
    assert result == []