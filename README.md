# Обработчик банковских операций

Модуль для фильтрации и сортировки банковских транзакций. Содержит две основные функции: `filter_by_state` для фильтрации операций по статусу и `sort_by_date` для сортировки операций по дате.

## Установка

### 1. Клонируйте репозиторий:

```
git clone https://github.com/Seregahck/project_one.git
cd project_one
```

2. Установите зависимости:
bash
pip install -r requirements.txt
Использование
python
from src.processing import filter_by_state, sort_by_date

# Тестовые данные
transactions = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
]

# Фильтрация по статусу EXECUTED
executed_transactions = filter_by_state(transactions, "EXECUTED")
print(f"Выполненные операции: {len(executed_transactions)}")

# Сортировка по дате (по умолчанию - по убыванию)
sorted_transactions = sort_by_date(transactions)
print(f"Последняя операция: {sorted_transactions[0]['date']}")

# Сортировка по возрастанию даты
ascending_transactions = sort_by_date(transactions, reverse=False)
print(f"Первая операция: {ascending_transactions[0]['date']}")
Дополнительные модули
Модуль masks.py
Функции для маскирования банковских данных:

python
from src.masks import get_mask_card_number, get_mask_account, mask_account_card

# Маскирование номера карты
card_number = "1234567890123456"
masked_card = get_mask_card_number(card_number)
print(f"Маскированная карта: {masked_card}")  # 1234 56** **** 3456

# Маскирование номера счета
account_number = "40817810570012345678"
masked_account = get_mask_account(account_number)
print(f"Маскированный счет: {masked_account}")  # **5678

# Автоматическое определение типа номера
text1 = "Visa 1234567890123456"
text2 = "Счет 40817810570012345678"
print(mask_account_card(text1))  # Visa 1234 56** **** 3456
print(mask_account_card(text2))  # Счет **5678
Модуль widget.py
Вспомогательные функции:

python
from src.widget import get_date

# Форматирование даты
iso_date = "2023-12-31T23:59:59"
formatted_date = get_date(iso_date)
print(f"Отформатированная дата: {formatted_date}")  # 31.12.2023
Описание функций
1. get_mask_card_number(card_number: str) -> str
Маскирует номер банковской карты в формате "XXXX XX** **** XXXX"

Тесты:

test_get_mask_card_number_valid - валидные номера карт

test_get_mask_card_number_invalid - невалидные номера

test_get_mask_card_number_with_spaces - номера с пробелами

2. get_mask_account(account_number: str) -> str
Маскирует номер банковского счета в формате "**XXXX"

Тесты:

test_get_mask_account_valid - валидные номера счетов

test_get_mask_account_invalid - невалидные номера

test_get_mask_account_with_spaces - номера с пробелами

3. mask_account_card(text: str) -> str
Определяет тип номера (карта или счет) и маскирует его

Тесты:

test_mask_account_card_card - строки с номерами карт

test_mask_account_card_account - строки с номерами счетов

test_mask_account_card_edge_cases - крайние случаи

4. get_date(date_str: str) -> str
Преобразует дату из формата ISO в формат "DD.MM.YYYY"

Тесты:

test_get_date_valid - валидные даты

test_get_date_invalid - невалидные даты

5. filter_by_state(transactions: List[Dict], state: str = "EXECUTED") -> List[Dict]
Фильтрует список транзакций по статусу

Тесты:

test_filter_by_state_basic - базовый тест фильтрации

test_filter_by_state_default - тест значения по умолчанию

test_filter_by_state_all_executed - все транзакции EXECUTED

test_filter_by_state_pending - фильтрация PENDING

test_filter_by_state_empty - пустой список

test_filter_by_state_single - одна транзакция

test_filter_by_state_parametrized - параметризованный тест

6. sort_by_date(transactions: List[Dict], reverse: bool = True) -> List[Dict]
Сортирует транзакции по дате

Тесты:

test_sort_by_date_descending - сортировка по убыванию

test_sort_by_date_ascending - сортировка по возрастанию

test_sort_by_date_chronological - хронологический порядок

test_sort_by_date_same_date - одинаковые даты

test_sort_by_date_empty - пустой список

test_sort_by_date_single - одна транзакция

test_sort_by_date_parametrized - параметризованный тест

Фикстуры
В файле tests/conftest.py определены фикстуры для тестов:

Для тестов маскирования:
valid_card_numbers - валидные номера карт

invalid_card_numbers - невалидные номера карт

valid_account_numbers - валидные номера счетов

invalid_account_numbers - невалидные номера счетов

card_strings - строки с картами

account_strings - строки со счетами

Для тестов дат:
valid_dates - валидные даты

invalid_dates - невалидные даты

Для тестов транзакций:
sample_transactions - образец транзакций

executed_transactions - только EXECUTED

pending_transactions - только PENDING

empty_transactions - пустой список

single_transaction - одна транзакция

dated_transactions - транзакции с датами

chronological_transactions - хронологический порядок

same_date_transactions - одинаковые даты

Запуск тестов
bash
# Запуск всех тестов
pytest

# Запуск с подробным выводом
pytest -v

# Запуск конкретного тестового файла
pytest tests/test_masks.py

# Запуск тестов с покрытием
coverage run -m pytest
coverage html -d coverage_report
Проверка качества кода
bash
# Проверка стиля кода
flake8 src tests

# Проверка типов
mypy src/

# Проверка безопасности
bandit -r src/

# filter_by_currency(transactions, currency_code)

Фильтрует транзакции по указанной валюте.

Параметры:

transactions (List[Dict[str, Any]]): Список транзакций в формате словарей

currency_code (str): Код валюты для фильтрации (например, "USD", "EUR")

Возвращает:

Iterator[Dict[str, Any]]: Генератор транзакций в указанной валюте

Пример:

python
transactions = [
    {"operationAmount": {"currency": {"code": "USD"}}, "description": "Payment 1"},
    {"operationAmount": {"currency": {"code": "EUR"}}, "description": "Payment 2"},
    {"operationAmount": {"currency": {"code": "USD"}}, "description": "Payment 3"},
]

usd_transactions = list(filter_by_currency(transactions, "USD"))

# transaction_descriptions(transactions)

Извлекает описания из списка транзакций.

Параметры:

transactions (List[Dict[str, Any]]): Список транзакций

Возвращает:

Iterator[str]: Генератор описаний транзакций

Пример:

python
transactions = [
    {"description": "Payment for groceries"},
    {"description": "Restaurant bill"},
    {"description": "Online shopping"},
]

descriptions = list(transaction_descriptions(transactions))

# card_number_generator(start, stop)

Генерирует номера банковских карт в указанном диапазоне.

Параметры:

start (int): Начальный номер карты (от 1)

stop (int): Конечный номер карты (до 9999999999999999)

Возвращает:

Generator[str, None, None]: Генератор номеров карт в формате "XXXX XXXX XXXX XXXX"

Исключения:

ValueError: Если параметры вне допустимого диапазона

Пример:

python
card_numbers = list(card_number_generator(1, 3))
# ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]

# Особенности
Работа с неполными данными
Функции корректно обрабатывают транзакции без ожидаемых полей

При отсутствии поля возвращаются пустые значения или пропускаются транзакции

Производительность
Используются генераторы для экономии памяти

Поддерживает обработку больших объемов данных

Обработка ошибок
card_number_generator проверяет корректность входных параметров

Все функции имеют аннотации типов для статической проверки