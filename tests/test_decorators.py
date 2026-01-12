import pytest
import os
import tempfile
from src.decorators import logit g


# Тестирование вывода в консоль
def test_log_to_console_success(capsys):
    """Тест успешного выполнения функции с выводом в консоль."""

    @log()
    def test_func(a, b):
        return a + b

    result = test_func(2, 3)

    captured = capsys.readouterr()
    output = captured.out

    assert result == 5
    assert "test_func ok" in output
    assert "error" not in output


def test_log_to_console_error(capsys):
    """Тест обработки ошибки с выводом в консоль."""

    @log()
    def test_func():
        raise ValueError("Test error")

    with pytest.raises(ValueError):
        test_func()

    captured = capsys.readouterr()
    output = captured.out

    assert "test_func error" in output
    assert "ValueError" in output
    assert "Test error" in output


# Тестирование записи в файл
def test_log_to_file_success():
    """Тест успешного выполнения функции с записью в файл."""

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp:
        filename = tmp.name

    try:
        @log(filename=filename)
        def test_func(x, y, z=10):
            return x * y + z

        result = test_func(2, 3, z=5)

        # Проверяем результат функции
        assert result == 11  # 2 * 3 + 5

        # Читаем содержимое файла
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        # Проверяем запись в файл
        assert "test_func ok" in content
        assert "error" not in content

    finally:
        # Удаляем временный файл
        os.unlink(filename)


def test_log_to_file_error():
    """Тест обработки ошибки с записью в файл."""

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp:
        filename = tmp.name

    try:
        @log(filename=filename)
        def test_func(a, b, c=0):
            if c == 0:
                raise RuntimeError("Cannot divide by zero")
            return a / c + b

        with pytest.raises(RuntimeError):
            test_func(10, 5, c=0)

        # Читаем содержимое файла
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        # Проверяем запись об ошибке в файл
        assert "test_func error" in content
        assert "RuntimeError" in content
        assert "Cannot divide by zero" in content

    finally:
        # Удаляем временный файл
        os.unlink(filename)


def test_log_with_different_arguments():
    """Тест с различными типами аргументов."""

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp:
        filename = tmp.name

    try:
        @log(filename=filename)
        def test_func(*args, **kwargs):
            return f"Args: {args}, Kwargs: {kwargs}"

        result = test_func(1, "two", [3, 4], key="value", number=42)

        # Проверяем результат
        assert "Args: (1, 'two', [3, 4])" in result
        assert "Kwargs: {'key': 'value', 'number': 42}" in result

        # Проверяем запись в файл
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        assert "test_func ok" in content

    finally:
        os.unlink(filename)


def test_log_preserves_function_metadata():
    """Тест, что декоратор сохраняет метаданные оригинальной функции."""

    @log()
    def original_func(x: int, y: int) -> int:
        """Тестовая функция для проверки метаданных."""
        return x + y

    # Проверяем сохранение имени
    assert original_func.__name__ == "original_func"

    # Проверяем сохранение документации
    assert "Тестовая функция для проверки метаданных" in original_func.__doc__

    # Проверяем сохранение аннотаций
    assert original_func.__annotations__ == {'x': int, 'y': int, 'return': int}


def test_log_without_filename_argument():
    """Тест использования декоратора без указания filename."""

    @log
    def test_func():
        return "test"

    # Проверяем, что функция корректно создалась
    assert callable(test_func)

    # Проверяем выполнение (логи будут в консоль)
    result = test_func()
    assert result == "test"


