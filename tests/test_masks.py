import pytest

from src.masks import get_mask_account, get_mask_card_number


def test_valid_card_masking():
    """Тест корректного маскирования стандартного номера карты"""
    # Тест без пробелов
    assert get_mask_card_number("1234567890123456") == "1234 56** **** 3456"
    # Тест с пробелами
    assert get_mask_card_number("1234 5678 9012 3456") == "1234 56** **** 3456"
    # Другой номер для проверки
    assert get_mask_card_number("1111222233334444") == "1111 22** **** 4444"


def test_invalid_length():
    """Тест неправильной длины номера карты"""
    # Слишком короткий номер
    with pytest.raises(ValueError, match="Номер карты должен состоять из 16 цифр."):
        get_mask_card_number("123456789012345")  # 15 цифр

    # Слишком длинный номер
    with pytest.raises(ValueError, match="Номер карты должен состоять из 16 цифр."):
        get_mask_card_number("12345678901234567")  # 17 цифр


def test_non_digit_characters():
    """Тест нецифровых символов в номере карты"""
    with pytest.raises(ValueError, match="Номер карты должен содержать только цифры"):
        get_mask_card_number("1234-5678-9012-3456")

    with pytest.raises(ValueError, match="Номер карты должен содержать только цифры"):
        get_mask_card_number("1234ABCD90123456")

    with pytest.raises(ValueError, match="Номер карты должен содержать только цифры"):
        get_mask_card_number("1234 5678 9012 345a")


def test_edge_cases():
    """Тест граничных случаев"""
    # Пустая строка
    with pytest.raises(ValueError):
        get_mask_card_number("")

    # Только пробелы
    with pytest.raises(ValueError, match="Номер карты должен содержать только цифры"):
        get_mask_card_number("    ")

    # Номер с разным количеством пробелов
    assert get_mask_card_number("1234  5678  9012  3456") == "1234 56** **** 3456"
    assert get_mask_card_number(" 1234567890123456 ") == "1234 56** **** 3456"


def test_special_cases():
    """Тест специальных случаев"""
    # Все нули
    assert get_mask_card_number("0000000000000000") == "0000 00** **** 0000"

    # Номер начинающийся с нулей
    assert get_mask_card_number("0123456789012345") == "0123 45** **** 2345"


def test_input_formats():
    """Тест различных форматов ввода"""
    # Разные форматы пробелов
    assert get_mask_card_number("1234 567890 123456") == "1234 56** **** 3456"
    assert get_mask_card_number("12345678 90123456") == "1234 56** **** 3456"

    # Табуляция (если бы была разрешена)
    with pytest.raises(ValueError):
        get_mask_card_number("1234\t5678\t9012\t3456")


def test_output_format():
    """Проверка точного формата вывода"""
    result = get_mask_card_number("1234567890123456")

    # Проверка длины результата (19 символов: 16 цифр + 3 пробела)
    assert len(result) == 19

    # Проверка позиций пробелов
    assert result[4] == " "
    assert result[9] == " "
    assert result[14] == " "

    # Проверка замаскированных частей
    parts = result.split(" ")
    assert parts[0] == "1234"
    assert parts[1] == "56**"
    assert parts[2] == "****"
    assert parts[3] == "3456"
