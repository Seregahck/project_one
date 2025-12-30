import pytest

from src.masks import get_mask_account, get_mask_card_number
from src.widget import mask_account_card, get_date



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


def test_valid_account_masking():
    """Тест корректного маскирования стандартного номера счета"""
    # Стандартный 20-значный счет (как в РФ)
    assert get_mask_account("40817810570012345678") == "**5678"
    assert get_mask_account("42305810678901234567") == "**4567"

    # Счет с пробелами
    assert get_mask_account("4081 7810 5700 1234 5678") == "**5678"
    assert get_mask_account("4230 5810 6789 0123 4567") == "**4567"


def test_minimum_length():
    """Тест минимальной длины счета (4 цифры)"""
    assert get_mask_account("1234") == "**1234"
    assert get_mask_account("5678") == "**5678"

    # С пробелами для минимальной длины
    assert get_mask_account("12 34") == "**1234"


def test_different_lengths():
    """Тест разных длин номеров счетов"""
    # 5 цифр
    assert get_mask_account("12345") == "**2345"
    # 10 цифр
    assert get_mask_account("1234567890") == "**7890"
    # 15 цифр
    assert get_mask_account("123456789012345") == "**2345"
    # 25 цифр (длиннее стандартного)
    assert get_mask_account("1234567890123456789012345") == "**2345"


def test_invalid_length():
    """Тест неправильной длины номера счета"""
    # Меньше 4 цифр
    with pytest.raises(ValueError, match="Номер счета должен быть длиной не менее 4 цифр"):
        get_mask_account("123")  # 3 цифры

    with pytest.raises(ValueError, match="Номер счета должен быть длиной не менее 4 цифр"):
        get_mask_account("")  # пустая строка

    with pytest.raises(ValueError, match="Номер счета должен быть длиной не менее 4 цифр"):
        get_mask_account("12")  # 2 цифры

    with pytest.raises(ValueError, match="Номер счета должен быть длиной не менее 4 цифр"):
        get_mask_account("1")  # 1 цифра


def test_non_digit_characters():
    """Тест нецифровых символов в номере счета"""
    with pytest.raises(ValueError, match="Номер счета должен содержать только цифры"):
        get_mask_account("4081-7810-5700-1234-5678")

    with pytest.raises(ValueError, match="Номер счета должен содержать только цифры"):
        get_mask_account("4081AB10570012345678")

    with pytest.raises(ValueError, match="Номер счета должен содержать только цифры"):
        get_mask_account("4081 7810 5700 1234 567a")


def test_edge_cases():
    """Тест граничных случаев"""
    # Только пробелы
    with pytest.raises(ValueError, match="Номер счета должен содержать только цифры"):
        get_mask_account("    ")

    # Пробелы в начале и конце
    assert get_mask_account(" 40817810570012345678 ") == "**5678"
    assert get_mask_account("  1234  ") == "**1234"

    def test_mask_account_card_credit_card():
        """Тест маскирования кредитной карты"""
        # Стандартный формат с разными типами карт
        assert mask_account_card("Visa Platinum 1234567890123456") == "Visa Platinum 1234 56** **** 3456"
        assert mask_account_card("MasterCard 1111222233334444") == "MasterCard 1111 22** **** 4444"
        assert mask_account_card("МИР 1234123412341234") == "МИР 1234 12** **** 1234"
        assert mask_account_card(
            "American Express 123456789012345") == "American Express 123456789012345"  # 15 цифр - не маскируется
        assert mask_account_card("Карта Сбербанка 5555666677778888") == "Карта Сбербанка 5555 66** **** 8888"

        # Карта с пробелами в номере (пробелы удаляются перед проверкой)
        assert mask_account_card("Visa 1234 5678 9012 3456") == "Visa 1234 56** **** 3456"
        assert mask_account_card("Карта 1111 2222 3333 4444") == "Карта 1111 22** **** 4444"
        assert mask_account_card("Master Card 9999 8888 7777 6666") == "Master Card 9999 88** **** 6666"

    def test_mask_account_card_account():
        """Тест маскирования банковского счета"""
        # Счет в разных регистрах
        assert mask_account_card("Счет 12345678901234567890") == "Счет **7890"
        assert mask_account_card("СЧЕТ 40817810570012345678") == "СЧЕТ **5678"
        assert mask_account_card("счет 42305810678901234567") == "счет **4567"
        assert mask_account_card("Банковский счет 12345678901234567890") == "Банковский счет **7890"
        assert mask_account_card("Расчетный счет 11112222333344445555") == "Расчетный счет **5555"

        # Счет с пробелами в номере
        assert mask_account_card("Счет 1234 5678 9012 3456 7890") == "Счет **7890"
        assert mask_account_card("Счет 4081 7810 5700 1234 5678") == "Счет **5678"
        assert mask_account_card("Счет 1234 5678 9012 3456") == "Счет **3456"  # 16 цифр, но это счет

    def test_mask_account_card_short_numbers():
        """Тест коротких номеров"""
        # Счет с коротким номером (менее 4 цифр)
        assert mask_account_card("Счет 123") == "Счет 123"
        assert mask_account_card("Счет 12") == "Счет 12"
        assert mask_account_card("Счет 1") == "Счет 1"
        assert mask_account_card("Счет") == "Счет"  # Только слово "Счет"

        # Карта с коротким номером
        assert mask_account_card("Visa 123456789012345") == "Visa 123456789012345"  # 15 цифр
        assert mask_account_card("Card 1234") == "Card 1234"  # 4 цифры
        assert mask_account_card("Карта 12345678901234567") == "Карта 12345678901234567"  # 17 цифр
        assert mask_account_card("Visa") == "Visa"  # Только слово "Visa"

    def test_mask_account_card_empty_and_invalid():
        """Тест пустых и некорректных входных данных"""
        # Пустая строка
        assert mask_account_card("") == ""

        # Только пробелы
        assert mask_account_card("   ") == ""
        assert mask_account_card("  ") == ""
        assert mask_account_card(" ") == ""

        # Только тип без номера
        assert mask_account_card("Visa") == "Visa"
        assert mask_account_card("Счет") == "Счет"
        assert mask_account_card("MasterCard Gold") == "MasterCard Gold"
        assert mask_account_card("Кредитная карта") == "Кредитная карта"

        # Номер с нецифровыми символами
        assert mask_account_card("Visa 1234-5678-9012-3456") == "Visa 1234-5678-9012-3456"
        assert mask_account_card("Счет 4081-7810-5700-1234") == "Счет 4081-7810-5700-1234"
        assert mask_account_card("Visa 1234abcd90123456") == "Visa 1234abcd90123456"
        assert mask_account_card("Счет AB1234567890") == "Счет AB1234567890"

        # Номер с пробелами и нецифровыми символами
        assert mask_account_card("Visa 1234 5678-9012 3456") == "Visa 1234 5678-9012 3456"

    def test_mask_account_card_mixed_spacing():
        """Тест различного форматирования пробелов"""
        # Множественные пробелы между словами
        assert mask_account_card("Visa   Platinum   1234567890123456") == "Visa Platinum 1234 56** **** 3456"
        assert mask_account_card("Счет   12345678901234567890") == "Счет **7890"

        # Пробелы в начале и конце
        assert mask_account_card("  Visa 1234567890123456  ") == "Visa 1234 56** **** 3456"
        assert mask_account_card("  Счет 12345678901234567890  ") == "Счет **7890"
        assert mask_account_card("   Карта Тинькофф 1234567890123456   ") == "Карта Тинькофф 1234 56** **** 3456"

        # Табуляция и другие пробельные символы (обрабатываются как пробелы)
        assert mask_account_card("\tVisa\t1234567890123456") == "Visa 1234 56** **** 3456"
        assert mask_account_card("Счет\t\t12345678901234567890") == "Счет **7890"

