# Обработчик банковских операций

## Модуль для фильтрации и сортировки банковских транзакций. Модуль содержит две основные функции: filter_by_state для фильтрации операций по статусу и sort_by_date для сортировки операций по дате.

## Установка:
1. Клонируйте репозиторий:
```
 [GitHub] https://github.com/Seregahck/project_one.git
```
2. Установите зависимости:
```
pip install -r requirements.txt
```
## Использование:

from processing import filter_by_state, sort_by_date

# Тестовые данные
transactions = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
]

## Декоратор log для логирования функций
Декоратор для логирования начала и конца выполнения функций с возможностью записи в файл или вывода в консоль.

# Особенности
Логирует время выполнения функции

Записывает успешное выполнение или ошибки

Поддерживает аргументы функций в логах

Сохраняет метаданные оригинальной функции (использует functools.wraps)

Имеет два режима работы: вывод в консоль или запись в файл

# Установка
Просто скопируйте код декоратора в свой проект:

python
import functools
from datetime import datetime
from typing import Optional, Any, Callable

 Вставьте код декоратора log здесь
# Использование
Базовое использование (вывод в консоль)
python
@log()
def add(a, b):
    return a + b

result = add(10, 5)  # Выведет в консоль: "2024-01-14 12:00:00 - add ok"
## Логирование в файл
python
@log("app.log")
def multiply(x, y):
    return x * y

result = multiply(3, 4)  # Запишет в файл app.log
## Декоратор с функциями, которые могут вызывать исключения
python
@log("errors.log")
def divide(a, b):
    return a / b

try:
    result = divide(10, 0)  # Запишет ошибку в файл errors.log
except ZeroDivisionError:
    pass
# Формат логов
## Успешное выполнение
text
2024-01-14 12:00:00 - function_name ok
## Ошибка выполнения
text
2024-01-14 12:00:00 - function_name error: ExceptionType: Error message. Inputs: args_tuple, kwargs_dict
# Примеры
# Пример 1: Простое логирование
python
@log()
def greet(name):
    return f"Hello, {name}!"

greet("Alice")  # Консоль: "2024-01-14 12:00:00 - greet ok"
# Пример 2: Логирование с аргументами
python
@log("operations.log")
def complex_calculation(x, y, coefficient=1.0):
    return (x + y) * coefficient

operations.log получит запись:
 "2024-01-14 12:00:00 - complex_calculation ok"
# Пример 3: Обработка ошибок
python
@log("app.log")
def read_file(filepath):
    with open(filepath, 'r') as f:
        return f.read()

try:
    content = read_file("nonexistent.txt")
except FileNotFoundError:
    # app.log получит запись вида:
    # "2024-01-14 12:00:00 - read_file error: FileNotFoundError: ... Inputs: ('nonexistent.txt',), {}"
    pass
# Параметры
Декоратор log
filename (str, optional): Имя файла для записи логов. Если не указан или None, логи выводятся в консоль.

# Преимущества
Универсальность: Работает с любыми функциями

Гибкость: Консольный вывод или файловое хранение

Информативность: Включает временные метки, имена функций, аргументы и трассировку ошибок

Безопасность: Сохраняет оригинальные исключения

Совместимость: Сохраняет метаданные функций (name, doc и т.д.)

# Ограничения
Логирует только начало выполнения (фактически - конец выполнения, так как время фиксируется в начале)

Не измеряет продолжительность выполнения функции

Для очень высоконагруженных приложений может потребоваться оптимизация

# Тестирование
Декоратор можно протестировать следующим образом:

python
import tempfile
import os

def test_log_decorator():
    # Тестирование консольного вывода
    @log()
    def test_func():
        return "test"
    
    # Тестирование файлового вывода
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
        tmp_file = tmp.name
    
    try:
        @log(tmp_file)
        def failing_func():
            raise ValueError("Test error")
        
        try:
            failing_func()
        except ValueError:
            pass
        
        # Проверяем содержимое файла
        with open(tmp_file, 'r') as f:
            content = f.read()
            assert "error" in content.lower()
    finally:
        os.unlink(tmp_file)

# Обработка финансовых транзакций

Проект для обработки и конвертации финансовых транзакций.

## Установка

1. Клонируйте репозиторий
2. Установите зависимости:

poetry install

## Создайте файл .env на основе .env.example:


## Получите API ключ на apilayer.com

Добавьте ключ в файл .env

## Использование
python
from src.utils import load_transactions
from src.external_api import get_transaction_amount_in_rub

# Загрузка транзакций
transactions = load_transactions('data/operations.json')

# Конвертация суммы в рубли
for transaction in transactions:
    try:
        amount_rub = get_transaction_amount_in_rub(transaction)
        print(f"Сумма в рублях: {amount_rub}")
    except Exception as e:
        print(f"Ошибка обработки транзакции: {e}")

## Запуск тестов

poetry run pytest tests/

# Структура проекта

src/utils.py - функции для работы с файлами

src/external_api.py - функции для работы с API

tests/ - модульные тесты

data/operations.json - данные транзакций

.env - конфигурация (не коммитится)

.env.example - шаблон конфигурации

src/utils.py - функции для работы с файлами

src/external_api.py - функции для работы с API

tests/ - модульные тесты

data/operations.json - данные транзакций

.env - конфигурация (не коммитится)

.env.example - шаблон конфигурации

## 9. Пример использования
```python
# main.py
from src.utils import load_transactions
from src.external_api import get_transaction_amount_in_rub

def main():
    # Загружаем транзакции
    transactions = load_transactions('data/operations.json')
    
    print(f"Загружено транзакций: {len(transactions)}")
    
    # Обрабатываем каждую транзакцию
    for i, transaction in enumerate(transactions[:5], 1):  # Первые 5 для примера
        try:
            amount_rub = get_transaction_amount_in_rub(transaction)
            currency = transaction.get('currency', 'N/A')
            original_amount = transaction.get('amount', 'N/A')
            
            print(f"Транзакция {i}:")
            print(f"  Исходная сумма: {original_amount} {currency}")
            print(f"  В рублях: {amount_rub:.2f} RUB")
            print("-" * 30)
            
        except Exception as e:
            print(f"Ошибка обработки транзакции {i}: {e}")

if __name__ == "__main__":
    main()
```

# Модуль чтения финансовых операций
Модуль для чтения финансовых операций из CSV и Excel файлов с поддержкой обработки ошибок и преобразования типов.

## Функции
read_csv_transactions(file_path: str) -> List[Dict[str, Any]]
Читает финансовые операции из CSV файла.

## Параметры:
file_path (str): Путь к CSV файлу

## Возвращает:
List[Dict[str, Any]]: Список словарей с транзакциями, где пустые значения преобразованы в None

## Исключения:
FileNotFoundError: Если файл не найден по указанному пути

ValueError: Если файл пуст, не содержит заголовков или имеет некорректный формат

## Пример использования:
python
from transaction_reader import read_csv_transactions

try:
    transactions = read_csv_transactions("operations.csv")
    for transaction in transactions:
        print(transaction)
except FileNotFoundError as e:
    print(f"Файл не найден: {e}")
except ValueError as e:
    print(f"Ошибка данных: {e}")
read_excel_transactions(file_path: str, sheet_name: Union[str, int] = 0) -> List[Dict[str, Any]]
Читает финансовые операции из Excel файла.

## Параметры:
file_path (str): Путь к Excel файлу

sheet_name (Union[str, int], optional): Название или индекс листа. По умолчанию 0 (первый лист)

## Возвращает:
List[Dict[str, Any]]: Список словарей с транзакциями, где NaN/NaT значения преобразованы в None

## Исключения:
FileNotFoundError: Если файл не найден по указанному пути

ValueError: Если файл пуст, лист не существует или имеет некорректный формат

## Пример использования:
python
from transaction_reader import read_excel_transactions

## Чтение первого листа
transactions1 = read_excel_transactions("operations.xlsx")

## Чтение листа по имени
transactions2 = read_excel_transactions("operations.xlsx", sheet_name="2024")

## Чтение листа по индексу
transactions3 = read_excel_transactions("operations.xlsx", sheet_name=1)
Особенности
Обработка пустых значений
В CSV файлах: пустые строки ("") преобразуются в None

В Excel файлах: значения NaN и NaT преобразуются в None

## Кодировка
CSV файлы читаются с кодировкой UTF-8

Excel файлы обрабатываются с автоматическим определением кодировки