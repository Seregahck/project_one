import json
import logging
import os
from typing import Any, Dict, List

# Создание логгера для модуля utils
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Создаем папку logs если она не существует
log_dir = "logs"
if not os.path.exists(log_dir):
    try:
        os.makedirs(log_dir, exist_ok=True)
        logger.debug(f"Создана папка для логов: {log_dir}")
    except Exception as e:
        print(f"Не удалось создать папку для логов: {e}")
        # Продолжаем без записи в файл
        pass

# Создание file handler для записи логов в файл
file_handler = logging.FileHandler(os.path.join(log_dir, "utils.log"), encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# Создание форматтера для логов
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(file_formatter)

# Добавление handler к логгеру
logger.addHandler(file_handler)


def load_transactions(file_path: str = "data/operations.json") -> List[Dict[str, Any]]:
    """
    Загружает транзакции из JSON-файла.

    Args:
        file_path: Путь до JSON-файла (по умолчанию "data/operations.json")

    Returns:
        Список словарей с данными о транзакциях
    """
    try:
        logger.debug(f"Начало загрузки транзакций из файла: {file_path}")

        # Проверяем существование файла
        if not os.path.exists(file_path):
            logger.warning(f"Файл не найден: {file_path}")
            return []

        # Проверяем, что файл не пустой
        if os.path.getsize(file_path) == 0:
            logger.warning(f"Файл пустой: {file_path}")
            return []

        # Открываем и читаем файл
        logger.debug(f"Чтение файла: {file_path}")
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Проверяем, что данные - это список
        if not isinstance(data, list):
            logger.warning(f"Данные в файле {file_path} не являются списком")
            return []

        logger.info(f"Успешно загружено {len(data)} транзакций из файла: {file_path}")
        return data

    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON в файле {file_path}: {str(e)}")
        return []
    except IOError as e:
        logger.error(f"Ошибка ввода-вывода при работе с файлом {file_path}: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Неожиданная ошибка при загрузке транзакций из {file_path}: {str(e)}")
        return []
