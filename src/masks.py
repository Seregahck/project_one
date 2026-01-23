import os
import logging
from typing import Optional

# Создание логгера для модуля masks
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Создаем папку logs если она не существует
log_dir = 'logs'
if not os.path.exists(log_dir):
    try:
        os.makedirs(log_dir, exist_ok=True)
        logger.debug(f"Создана папка для логов: {log_dir}")
    except Exception as e:
        print(f"Не удалось создать папку для логов: {e}")
        # Продолжаем без записи в файл
        pass

# Создание file handler для записи логов в файл
try:
    file_handler = logging.FileHandler(os.path.join(log_dir, 'masks.log'), encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    # Создание форматтера для логов
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)

    # Добавление handler к логгеру
    logger.addHandler(file_handler)

except (FileNotFoundError, PermissionError) as e:
    # Если не удалось создать файл лога, создаем StreamHandler
    print(f"Не удалось создать файл лога: {e}. Используется вывод в консоль.")
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    stream_handler.setFormatter(stream_formatter)
    logger.addHandler(stream_handler)
    logger.warning("Файл лога недоступен. Логи выводятся в консоль.")


def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты в формате XXXX XX** **** XXXX

    Args:
        card_number: Номер карты (16 цифр, пробелы игнорируются)

    Returns:
        Замаскированный номер карты в формате XXXX XX** **** XXXX

    Raises:
        ValueError: Если номер карты невалидный
    """
    try:
        logger.debug(f"Начало маскировки номера карты: {card_number}")

        # Убираем пробелы
        cleaned_number = card_number.replace(" ", "")

        # Валидация
        if not cleaned_number.isdigit():
            error_msg = "Номер карты должен содержать только цифры"
            logger.error(f"{error_msg}. Входные данные: {card_number}")
            raise ValueError(error_msg)

        if len(cleaned_number) != 16:
            error_msg = "Номер карты должен состоять из 16 цифр"
            logger.error(f"{error_msg}. Получено {len(cleaned_number)} цифр. Входные данные: {card_number}")
            raise ValueError(error_msg)

        # Разбиваем на части
        part1 = cleaned_number[:4]
        part2 = cleaned_number[4:6]
        part3 = "**"
        part4 = "****"
        part5 = cleaned_number[-4:]

        result = f"{part1} {part2}{part3} {part4} {part5}"

        logger.info(f"Успешная маскировка номера карты: {card_number} -> {result}")
        return result

    except ValueError as e:
        # ValueError уже залогирован выше
        raise
    except Exception as e:
        error_msg = f"Неожиданная ошибка при маскировке номера карты: {str(e)}"
        logger.error(f"{error_msg}. Входные данные: {card_number}")
        raise RuntimeError(error_msg) from e


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счета в формате **XXXX

    Args:
        account_number: Номер счета (минимум 4 цифры, пробелы игнорируются)

    Returns:
        Замаскированный номер счета в формате **XXXX

    Raises:
        ValueError: Если номер счета невалидный
    """
    try:
        logger.debug(f"Начало маскировки номера счета: {account_number}")

        # Убираем пробелы
        cleaned_number = account_number.replace(" ", "")

        # Валидация
        if not cleaned_number.isdigit():
            error_msg = "Номер счета должен содержать только цифры"
            logger.error(f"{error_msg}. Входные данные: {account_number}")
            raise ValueError(error_msg)

        if len(cleaned_number) < 4:
            error_msg = f"Номер счета должен быть длиной не менее 4 цифр. Получено {len(cleaned_number)} цифр"
            logger.error(f"{error_msg}. Входные данные: {account_number}")
            raise ValueError(error_msg)

        result = f"**{cleaned_number[-4:]}"

        logger.info(f"Успешная маскировка номера счета: {account_number} -> {result}")
        return result

    except ValueError as e:
        # ValueError уже залогирован выше
        raise
    except Exception as e:
        error_msg = f"Неожиданная ошибка при маскировке номера счета: {str(e)}"
        logger.error(f"{error_msg}. Входные данные: {account_number}")
        raise RuntimeError(error_msg) from e


def mask_card_or_account(number: str) -> Optional[str]:
    """
    Автоматически определяет тип номера (карта или счет) и применяет соответствующую маскировку.

    Args:
        number: Номер карты или счета

    Returns:
        Замаскированный номер или None в случае ошибки
    """
    try:
        logger.debug(f"Автоматическое определение типа номера: {number}")

        # Убираем пробелы
        cleaned_number = number.replace(" ", "")

        if not cleaned_number.isdigit():
            logger.warning(f"Номер содержит не только цифры: {number}")
            return None

        if len(cleaned_number) == 16:
            # Это номер карты
            result = get_mask_card_number(number)
            logger.info(f"Автоматически определен как номер карты: {number} -> {result}")
        else:
            # Это номер счета
            result = get_mask_account(number)
            logger.info(f"Автоматически определен как номер счета: {number} -> {result}")

        return result

    except Exception as e:
        logger.error(f"Ошибка при автоматической маскировке номера {number}: {str(e)}")
        return None
